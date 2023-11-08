from pydantic import BaseModel
from models.user.user import User
class Confirm(BaseModel):
    response:bool
    user:User
    detail:str