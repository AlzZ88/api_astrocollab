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


# Configuración de las políticas de CORS
origins = [
    "192.168.6.248",  # Reemplaza con la URL de tu aplicación web
    "http://astrocollab.inf.udec.cl",
    "https://astrocollab.inf.udec.cl",
    # Agrega más orígenes permitidos si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Puedes especificar los métodos HTTP permitidos
    allow_headers=["*"],  # Puedes especificar los encabezados permitidos
)

# Configurar FastAPI
@app.on_event("startup")

async def startup_db_client():
    pass
    
    #create_tables()

app.include_router(corrections_router, prefix="/api/corrections")
app.include_router(objects_router, prefix="/api/objects")
app.include_router(ad_router, prefix="/api/ads")
app.include_router(users_router, prefix="/api/users")
app.include_router(project_router,prefix="/api/projects")


db_handler = AlerceDataBaseHandler()


@app.get("/api/")
def index():
    return "Astrocollab 1.1.0"


# Manejo de errores generales
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})
