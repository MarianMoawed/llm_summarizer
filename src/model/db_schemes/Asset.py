from pydantic import BaseModel,Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class Asset(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    asset_type:str = Field(...)
    asset_name:str = Field(...)
    asset_pushed_at: datetime = Field(default=datetime.now)
    asset_project_id: str = Field(...)


    @classmethod
    def get_indexes(cls):
        return [{
            "key":[("asset_project_id", 1)],
            "name": "asset_project_id_index_1",
            "unique": False
        }]


    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }
    