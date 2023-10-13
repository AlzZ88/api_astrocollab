from fastapi import APIRouter, HTTPException, Depends
from models.confirm.confirm import Confirm
from models.ad.ad import Ad
from schemas.ad_sc.ad_sc import AdSchema
from typing import List
from data.database_handler import get_db
from sqlalchemy.orm import Session
ad_router = APIRouter()


@ad_router.get("/", response_model=List[Ad])
async def get_ads(db: Session = Depends(get_db)):
    ads = db.query(AdSchema).all()
    return ads

@ad_router.delete("/{ad_id}")
async def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(AdSchema).filter(AdSchema.id == ad_id).first()
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    db.delete(ad)
    db.commit()
    return Confirm(response=True, detail="Correction inserted.")

# Ruta para agregar un nuevo anuncio
@ad_router.post("/", response_model=Ad)
async def add_ad(ad: Ad, db: Session = Depends(get_db)):
    db_ad = AdSchema(title=ad.title,description=ad.description,img=ad.img)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad