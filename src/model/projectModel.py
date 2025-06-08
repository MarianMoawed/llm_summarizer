from .BaseDataModel import BaseDataModel
from .enums.DBEnums import DBEnums
from .db_schemes.Project import Project
from bson import ObjectId

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.PROJECT_COLLECTION.value]

    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance
        
        


    async def init_collection(self):
        collections = await self.db_client.list_collection_names()
        if DBEnums.CHUNK_COLLECTION.value not in collections:
            self.collection = self.db_client[DBEnums.PROJECT_COLLECTION.value]

        indexes = Project.get_indexes()
        for index in indexes:
            await self.collection.create_index(index["key"],
                                        name = index["name"],
                                        unique = index["unique"])
       
    
    async def insert_project(self, project:Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True,exclude_unset=True))
        project.id=result.inserted_id
        return project
    
    async def get_project_by_id_or_create_one(self, project_id: str):
        project = await self.collection.find_one({"project_id": project_id})
        if project:
            
            return Project(**project)
        else:
            new_project = Project(project_id=project_id)
            await self.insert_project(new_project)
            return new_project


    async def get_all_projects(self, page:int=1, page_size:int=10):
        
        total_documents= await self.collection.count_documents({})

    
        total_pages=total_documents//page_size
        if total_documents % page_size > 0 :
            total_pages +=1
        
        cursor = self.collection.find().skip((page-1) * page_size).limit(page_size)
        projects = []

        async for document in cursor:
            projects.append(
                Project(**document)
            )
        return projects,total_pages



