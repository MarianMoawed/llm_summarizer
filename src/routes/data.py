from fastapi import APIRouter, Request, UploadFile, File, Form,status
from fastapi.responses import JSONResponse
from typing import Optional
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from model.enums.signalResponse import SignalResponse
from model.enums.AssetTypeEnums import AssetTypeEnums
from .Schemes.data import ChunkingScheme
from model.projectModel import ProjectModel
from model.AssetModel import AssetModel
from model.db_schemes.Asset import Asset
from model.db_schemes.Chunk import Chunk
from model.ChunkModel import ChunkModel
from bson import ObjectId
import json
from controllers.ProcessController import ProcessController


data_router = APIRouter(prefix="/api/v1",tags=["data"])


@data_router.post("/upload/text")
def upload_text(text: Optional[str] =None):
   if text:
        return {"text": text}
   


@data_router.post("/upload/file")
async def upload_file(request:Request, project_id:str, file: Optional[UploadFile]=File(None)):

   project_model =await ProjectModel.create_instance(request.app.db_client)
   asset_model = AssetModel(request.app.db_client)
   project = await project_model.get_project_by_id_or_create_one(project_id= project_id)
   

   data_controller= DataController(project_id=project_id, file=file)
   response =SignalResponse
   
   if file:
      is_valid= data_controller.is_supported_file_type(file=file)

   if is_valid:
      file_path, new_file_id=data_controller.create_unique_file_path(
         original_file_name=file.filename,
         project_id= project_id
         )
   else :
      return JSONResponse(
      status_code= 400,
      content={
         "signal":response.FILE_TYPE_NOT_SUPPORTED_ERROR.value
      }
   )
   asset = Asset(
      asset_type = AssetTypeEnums.FILE.value,
      asset_name = new_file_id,
      asset_project_id = project_id
   )

   await data_controller.save_uploaded_file(new_file_path=file_path,
                                             chunk_size=ChunkingScheme().chunk_size)
   await project_model.get_project_by_id_or_create_one(project_id)
   record = await asset_model.insert_asset(asset)

   return JSONResponse(
      content={
         "signal":response.FILE_UPLOADED_SUCCESSFULLY.value,
         "file_id :": new_file_id
      }
   )


@data_router.post("/process/{project_id}")
async def process_file(request:Request, project_id:str, chunk_settings:ChunkingScheme):
   
   chunk_size = chunk_settings.chunk_size
   overlap_size = chunk_settings.overlap_size

   project_model =await ProjectModel.create_instance(db_client= request.app.db_client)
   project =await project_model.get_project_by_id_or_create_one(project_id= project_id)

   chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

   asset_model = await AssetModel.create_instance(db_client= request.app.db_client)
   project_ids = {}
   if chunk_settings.file_id:
      asset_record = await asset_model.get_asset_record(asset_project_id= project_id, 
                                                        asset_name= chunk_settings.file_id)
      if asset_record == None:
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                             content={"signal":SignalResponse.FILE_ID_ERROR.value})
      project_ids = {asset_record.id:asset_record.asset_name}

   else:
      assets = await asset_model.get_project_assets(project_id=project_id,
                                                     asset_type=AssetTypeEnums.FILE.value)
      if len(assets) == 0:
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                 content={"signal":SignalResponse.FILE_ID_ERROR.value})
      for asset in assets:
         project_ids = {asset.id:asset.asset_name}
   
   if chunk_settings.do_reset == 1:
      deleted_chunks_count = await chunk_model.delete_project_chunks(project_id=project.id)
      return JSONResponse(
         status_code= status.HTTP_200_OK,
         content={
            "signal":SignalResponse.CHUNKS_DELETED_SUCCESSFULLY.value,
            "deleted_chunks_count":deleted_chunks_count
         }
      )
   
   no_records = 0
   no_files = 0

   for asset_id, file_id in project_ids.items():
      file_content = ProcessController(project_id=project_id).get_file_content(file_id=file_id)
      file_chunks = ProcessController(project_id=project_id).process_file(
      file_id=file_id,
      file_content=file_content,
      chunk_size=chunk_size,
      overlap_size=overlap_size,
      do_reset=0)

      file_chunks_record = [
         Chunk(chunk_content= chunk.page_content,
               chunk_metadata= json.dumps(chunk.metadata),
               chunk_order= i +1,
               chunk_project_id= project_id,
               asset_id= asset_id)
         for i, chunk in enumerate(file_chunks)
         ]
      
      no_records += await chunk_model.insert_many(chunks=file_chunks_record)
      no_files +=1
   return JSONResponse(status_code=status.HTTP_200_OK,
                       content={
                          "signal":SignalResponse.CHUNKS_INSERTED_SUCCESSFULLY.value,
                          "no_records":no_records,
                          "no_files":no_files
                       })
       

         



   

