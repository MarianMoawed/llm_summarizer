from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from model.enums.signalResponse import SignalResponse
from .Schemes.data import FileScheme


data_router = APIRouter(prefix="/api/v1",tags=["data"])


@data_router.post("/upload/text")
def upload_text(text: Optional[str] =None):
   if text:
        return {"text": text}
   


@data_router.post("/upload/file")
async def upload_file(project_id:str, file: Optional[UploadFile]=File(None)):

   data_controller= DataController(project_id=project_id, file=file)
   response =SignalResponse
   
   if file:
      is_valid= data_controller.is_supported_file_type(file=file)

   if is_valid:
      file_path, new_file_id=data_controller.create_unique_file_path(original_file_name=file.filename,
                                                         project_id= project_id)
   else :
      return JSONResponse(
      status_code= 400,
      content={
         "signal":response.FILE_TYPE_NOT_SUPPORTED_ERROR.value
      }
   )

   await data_controller.save_uploaded_file(new_file_path=file_path, chunk_size=FileScheme().chunk_size)
   return JSONResponse(
      content={
         "signal":response.FILE_UPLOADED_SUCCESSFULLY.value,
         "file_id :": new_file_id
      }
   )

