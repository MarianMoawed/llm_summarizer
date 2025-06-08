from pydantic import BaseModel,Field
from bson import ObjectId
from typing import Optional


class Chunk(BaseModel):
    id:Optional[ObjectId] = Field(None, alias="_id")
    chunk_content:str = Field(..., min_length=1)
    chunk_metadata:str
    chunk_order:int = Field(...)
    chunk_project_id:str
    asset_id: ObjectId


    @classmethod
    def get_indexes(cls):
        return [{
            "key":[("chunk_project_id", 1)],
            "name": "chunk_project_id_index_1",
            "unique": False
        }]


    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }
