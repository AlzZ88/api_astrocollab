from fastapi import FastAPI
from data.alerce_database_handler import AlerceDataBaseHandler
from fastapi.middleware.cors import CORSMiddleware
from data.database_handler import create_tables, get_db
from routes.corrections_routes import corrections_router
from routes.users_routes import users_router
from routes.objects_routes import objects_router
from routes.ad_routes import ad_router
from routes.projects_routes import project_router
from starlette.responses import JSONResponse


app = FastAPI()


# Configurar FastAPI
@app.on_event("startup")
async def startup_db_client():
    pass
    
    #create_tables()

app.include_router(corrections_router, prefix="/corrections")
app.include_router(objects_router, prefix="/objects")
app.include_router(ad_router, prefix="/ads")
app.include_router(users_router, prefix="/users")
app.include_router(project_router,prefix="/projects")


db_handler = AlerceDataBaseHandler()


@app.get("/")
def index():
    return "Astrocollab 1.1.0"


# Manejo de errores generales
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})
