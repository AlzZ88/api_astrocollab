from pydantic import BaseModel
class Ad(BaseModel):
    id:int
    title: str
    description: str
    img: str