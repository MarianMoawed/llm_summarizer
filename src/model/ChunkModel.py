from .BaseDataModel import BaseDataModel
from .enums.DBEnums import DBEnums 
from .db_schemes.Chunk import Chunk
from pymongo import InsertOne
from bson import ObjectId


class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.CHUNK_COLLECTION.value]

    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance
        
        


    async def init_collection(self):
        collections = await self.db_client.list_collection_names()
        if DBEnums.CHUNK_COLLECTION.value not in collections:
            self.collection = self.db_client[DBEnums.CHUNK_COLLECTION.value]

        indexes = Chunk.get_indexes()
        for index in indexes:
            await self.collection.create_index(keys=index["key"],
                                        name = index["name"],
                                        unique = index["unique"])




    async def insert_many(self,chunks:list[Chunk], batch_size:int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i: i + batch_size]
            docs = [chunk.model_dump(by_alias=True, exclude_unset=True) for chunk in batch]
            if docs:
                await self.collection.insert_many(docs)
        return len(chunks)
        
    
    async def delete_project_chunks(self, project_id:ObjectId):
        result = await self.collection.delete_many({"project_id":project_id})
        return result.deleted_count
    
    async def get_asset_chunks(self, project_id:str, asset_id:ObjectId):
        cursor = self.collection.find({"chunk_project_id":project_id,
                                             "asset_id":asset_id})
        result = await cursor.to_list(length=None)
        if result==None:
            return None
        return [ 
            Chunk(**chunk)
            for chunk in result
        ]
    

    async def get_project_chunks(self, project_id: ObjectId, page_num:int=1, page_size:int=50):
        result = await self.collection.find({
            "chunk_project_id": ObjectId(project_id)
        }).skip(

            (page_num-1 )*page_size
        ).limit(page_size).to_list(length=None)
        
        if result is None:
            return None
        return [Chunk(**chunk) for chunk in result]