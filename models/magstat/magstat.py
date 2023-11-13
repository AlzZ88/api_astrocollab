from typing import Optional
from pydantic import BaseModel

class MagStat(BaseModel):
    oid: str
    ndubiousG:Optional[int]
    magmeanG: Optional[float]  # Permitir valores nulos en campos de tipo float
    magmedianG: Optional[float]
    magmaxG: Optional[float]
    magminG: Optional[float]
    magsigmaG: Optional[float]
    maglastG: Optional[float]
    magfirstG: Optional[float]
    firstmdjG: Optional[float]
    lastmdjG: Optional[float]
    step_id_corrG: Optional[str]  # Permitir valores nulos en campos de tipo str

    ndubiousR: int
    magmeanR: Optional[float]
    magmedianR: Optional[float]
    magmaxR: Optional[float]
    magminR: Optional[float]
    magsigmaR: Optional[float]
    maglastR: Optional[float]
    magfirstR: Optional[float]
    firstmdjR: Optional[float]
    lastmdjR: Optional[float]
    step_id_corrR: Optional[str]