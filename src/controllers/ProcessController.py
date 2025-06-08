from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain.document_loaders import PyPDFium2Loader
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from model.enums.ProcessEnums import FielType
from model.enums.signalResponse import SignalResponse
import logging
import os





class ProcessController(BaseController):
    def __init__(self, project_id:str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id= project_id)

    def get_file_extension(self , file_id:str):
       extension = os.path.splitext(file_id )[-1]
       return extension
    
    def get_document_loader(self, file_id:str):
        ext = self.get_file_extension(file_id=file_id)
        if ext == FielType.PDF.value:
            return PyPDFium2Loader(os.path.join(self.project_path, file_id))
        if ext == FielType.TXT.value:
            return TextLoader(os.path.join(self.project_path , file_id), encoding= "utf-8")
        else:
            raise ValueError(f"{SignalResponse.FILE_TYPE_NOT_SUPPORTED_ERROR.value}: {ext}")
        
    def get_file_content(self, file_id:str):
        loader = self.get_document_loader(file_id= file_id)
        return loader.load()
    
    def process_file(self, file_content:list, file_id:str, chunk_size:int, overlap_size:int, do_reset:int):
        text_splitter = RecursiveCharacterTextSplitter("\n", chunk_size=chunk_size, chunk_overlap=overlap_size
                                                       )
        file_text = [

           rec.page_content
             for rec in file_content
        ]

        file_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(file_text, file_metadata)
        return chunks

