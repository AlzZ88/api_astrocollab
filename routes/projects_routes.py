from fastapi import APIRouter, HTTPException, Depends
from models.project.project import Project
from models.confirm.confirm import Confirm
from schemas.project_sc.project_sc import ProjectSchema
from data.database_handler import get_db
from sqlalchemy.orm import Session
from typing import List
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
        return Confirm(response=True, detail="")
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error: {e}")