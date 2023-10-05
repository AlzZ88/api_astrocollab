from pydantic import BaseModel
class Confirm(BaseModel):
    response:bool
    detail:str