from typing import List
from pydantic import BaseModel

class Project(BaseModel):
    pid:int
    name:str
    description:str
    labels:List[str]
    objects:List[str]

    def __str__(self):
        return f"Project(name={self.name}, description={self.description}, labels={self.labels}, objects={self.objects})"