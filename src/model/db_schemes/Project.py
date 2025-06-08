from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class Project(BaseModel):
    id:Optional[ObjectId] = Field(None, alias="_id")
    project_id:str = Field(..., min_length=1)





    @classmethod
    def get_indexes(cls):
        return [{
            "key":[("project_id", 1)],
            "name": "project_id_index_1",
            "unique": True
        }]
    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }