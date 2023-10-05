from pydantic import BaseModel
from typing import Optional
class ObjectBasic(BaseModel):
    oid: str
    discovery_date: Optional[float]
    last_detection: Optional[float]
    det: Optional[int]
    non_det: Optional[int]
    correct: Optional[bool]
    stellar: Optional[bool]