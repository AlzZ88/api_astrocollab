from pydantic import BaseModel

class User(BaseModel):
    privilege:bool
    mail: str
    username: str
    password: str
    