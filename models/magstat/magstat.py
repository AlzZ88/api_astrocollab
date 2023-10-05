from pydantic import BaseModel

class MagStat(BaseModel):
    oid:str
    ndubiousG: int
    magmeanG: float
    magmedianG: float
    magmaxG: float
    magminG: float
    magsigmaG: float
    maglastG: float
    magfirstG:float
    firstmdjG:float
    lastmdjG:float
    step_id_corrG: str

    ndubiousR: int
    magmeanR: float
    magmedianR: float
    magmaxR: float
    magminR: float
    magsigmaR: float
    maglastR: float
    magfirstR:float
    firstmdjR:float
    lastmdjR:float
    step_id_corrR: str