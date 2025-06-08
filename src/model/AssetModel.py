from .BaseDataModel import BaseDataModel
from .enums.DBEnums import DBEnums
from .db_schemes.Asset import Asset
from bson import ObjectId




class AssetModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = db_client[DBEnums.ASSET_COLLECTION.value]

    
    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        collections = await self.db_client.list_collection_names()
        if DBEnums.ASSET_COLLECTION.value not in collections:
            self.collection = self.db_client[DBEnums.ASSET_COLLECTION.value]
        indexes = Asset.get_indexes()
        for index in indexes:
           await self.collection.create_index( index["key"],
                                         name = index["name"],
                                         unique = index["unique"])
           
    async def insert_asset(self , asset:Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True ,
                                                                    exclude_unset=True))
        return str(result)
    
    
    async def get_project_assets(self, project_id: str, asset_type:str):
        records = self.collection.find({
           "asset_project_id":ObjectId(project_id)
            if isinstance(project_id, str)
            else project_id,
            "asset_type":asset_type
            }).to_list(length=None)
        assets =[]
        for record in records:
            assets.append(Asset(**record))

        return assets
           
                
    async def delete_asset(self, asset_id: str):
        await self.collection.delete_one({"_id": ObjectId(asset_id) if isinstance(asset_id, str) 
                                          else asset_id})

    async def get_asset_record(self,asset_project_id:str,asset_name:str):
        record =await self.collection.find_one({
            "asset_project_id":asset_project_id,
           "asset_name":asset_name
        })
        if record:
            return Asset(**record)
        return None