from pydantic import BaseModel

class MagStatR(BaseModel):
    oid:str
    ndubious: int
    magmean: float
    magmedian: float
    magmax: float
    magmin: float
    magsigma: float
    maglast: float
    magfirst:float
    firstmdj:float
    lastmdj:float
    step_id_corr: str    
