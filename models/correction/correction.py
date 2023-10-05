from pydantic import BaseModel
from typing import List
from models.comment.comment import Comment
class Correction(BaseModel):
    oid: str
    username:str
    pid:int
    label: str