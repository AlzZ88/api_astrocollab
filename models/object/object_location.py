from pydantic import BaseModel
from typing import Optional

class ObjectLocation(BaseModel):
    oid: str
    ra: Optional[float]
    dec: Optional[float]