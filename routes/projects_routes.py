from fastapi import APIRouter, HTTPException, Depends
from models.project.project import Project
from models.confirm.confirm import Confirm
from schemas.project_sc.project_sc import ProjectSchema
from schemas.correction_sc.correction_sc import CorrectionSchema
from sqlalchemy.orm.exc import NoResultFound
from data.database_handler import get_db
from sqlalchemy.orm import Session
from typing import List
from models.user.user import User
project_router = APIRouter()



@project_router.get("/", response_model=List[Project])
async def get_projects(db: Session = Depends(get_db)):
    """
    Get all projects.

    Args:
        db (Session): The database session.

    Returns:
        List[Project]: A list of Project objects.
    """
    db_projects = db.query(ProjectSchema).all()
    print(db_projects)
    if not db_projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return db_projects



@project_router.get("/labels/{oid}")
async def get_project_labels(oid: str, db: Session = Depends(get_db)):
    try:
        # Buscar el proyecto que tiene el OID proporcionado
        project = db.query(ProjectSchema).join(CorrectionSchema).filter(CorrectionSchema.oid == oid).one()
        return project.labels
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Project not found")


@project_router.get("/{pid}", response_model=List[Project])
async def get_projects(pid:int,db: Session = Depends(get_db)):
    """
    Get all projects.

    Args:
        db (Session): The database session.

    Returns:
        List[Project]: A list of Project objects.
    """
    db_projects = db.query(ProjectSchema).filter(ProjectSchema.pid == pid).all()
    print(db_projects)
    if not db_projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return db_projects



@project_router.post("/")
async def add_project(project:Project, db: Session = Depends(get_db)):
    try:
        db_project = ProjectSchema(
            name=project.name,
            description=project.description,
            labels=project.labels,
            objects=project.objects
        )
        print(db_project)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return Confirm(response=True, detail="",user=User(privilege=False,mail="",username="",password=""))

    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error: {e}",user=User(privilege=False,mail="",username="",password=""))



@project_router.put("/", response_model=Confirm)
async def update_project(project: Project, db: Session = Depends(get_db)):
    """
    Update project data by project_id.

    Args:
        project_id (int): The ID of the project to be updated.
        project (Project): The Project object with updated data.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating success or failure of the update.
    """
    try:
        db_project = db.query(ProjectSchema).filter(ProjectSchema.pid == project.pid).first()
        if not db_project:
            return Confirm(response=False, detail="The project does not exist",user=User(privilege=False,mail="",username="",password=""))


        # Actualiza los campos relevantes con los nuevos valores de la solicitud
        if project.name!="":
            db_project.name = project.name
        if project.description!="":
            db_project.description = project.description
        if len(project.labels)>0:
            db_project.labels = project.labels
        if len(project.objects)>0:
            db_project.objects = project.objects

        db.commit()
        db.refresh(db_project)

        return Confirm(response=True, detail="Project data updated successfully",user=User(privilege=False,mail="",username="",password=""))

    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error: {e}",user=User(privilege=False,mail="",username="",password=""))



