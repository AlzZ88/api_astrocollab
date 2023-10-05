from pydantic import BaseModel
class Ad(BaseModel):
    title: str
    description: str
    img: str