
from fastapi.responses import JSONResponse
from model.enums.signalResponse import SignalResponse
from controllers.ProjectController import ProjectController
from .BaseController import BaseController
from fastapi import UploadFile
import os,re
import aiofiles
import logging


class DataController(BaseController) :
    def __init__(self,project_id:str,file:UploadFile):
        super().__init__()
        self.file =file
        project_id=project_id

    def is_supported_file_type(self, file:UploadFile):
        if file.content_type not in self.settings.FILE_TYPES:
            return False
        else:
            return True
        
    def create_unique_file_path(self,original_file_name:str, project_id:str):

        random_key=self.generate_random_string(length=12)
        project_path= ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name= self.get_clean_file_name(original_file_name=original_file_name)

        new_file_path= os.path.join(
            project_path, random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key=self.generate_random_string(length=12)
            new_file_path= os.path.join(
            project_path, random_key + "_" + cleaned_file_name
        )
        
        return new_file_path, random_key + "_" + cleaned_file_name




    def get_clean_file_name(self, original_file_name:str):
        cleaned_file_name=re.sub(r'[^\w.]','',original_file_name.strip())

        cleaned_file_name= cleaned_file_name.replace(" ","_")

        return cleaned_file_name
    
    
        
    async def save_uploaded_file(self, new_file_path, chunk_size=1024*1024):
        try:
            async with aiofiles.open(new_file_path, "wb") as buffer:
                while True:
                    chunk = await self.file.read(chunk_size)
                    if not chunk:
                        break
                    await buffer.write(chunk)
            return new_file_path
        except Exception as e:
            logging.error(SignalResponse.FILE_SAVING_ERROR.value)
            return None
        
    
