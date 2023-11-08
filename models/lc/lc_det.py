from pydantic import BaseModel
from typing import List

class LightCurveDetection(BaseModel):
    fid: int
    mjd: float
    magpsf: float
    sigmapsf: float

class LightCurveNonDetection(BaseModel):
    fid: int
    mjd: float
    diffmaglim: float


class LightCurveData(BaseModel):
    detections: List[LightCurveDetection]
    non_detections: List[LightCurveNonDetection]