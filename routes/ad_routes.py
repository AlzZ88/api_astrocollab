from fastapi import APIRouter, HTTPException, Depends


ad_router = APIRouter()


# Simula una base de datos de anuncios
ads_db = []

# Ruta para obtener todos los anuncios
@ad_router.get("/anuncios")
async def get_ads():
    return ads_db
