from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class Todo(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    description: Optional[str] = None
    completed: bool = False


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
