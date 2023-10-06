from typing import List,Union
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.comment.comment import Comment
from models.confirm.confirm import Confirm
from models.correction.correction import Correction
from models.user.user import User
from schemas.comment_sc.comment_sc import CommentSchema
from schemas.correction_sc.correction_sc import CorrectionSchema
from schemas.user_sc.user_sc import UserSchema
from data.database_handler import get_db

# Create an APIRouter instance
corrections_router = APIRouter()

@corrections_router.get("/", response_model=List[Correction])
async def get_corrections(db: Session = Depends(get_db)):
    """
    Get user history.

    Args:
        user (str): The username.
        db (Session): The database session.

    Returns:
        List[HistoryItem]: A list of HistoryItem objects.
    """
    db_history = db.query(CorrectionSchema).all()
    if not db_history:
        raise HTTPException(status_code=404, detail="Corrections not found")
    return db_history



@corrections_router.post("/", response_model=Confirm)
async def post_object_correction(correction: Correction, db: Session = Depends(get_db)):
    """
    Post object correction.

    Args:
        correction (Correction): The Correction object containing object and project ID, the username and correction.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed correction posting.
    """
    try:
        db_correction = CorrectionSchema(oid=correction.oid, username=correction.username,pid=correction.pid, label=correction.label)
        db.add(db_correction)
        db.commit()
        db.refresh(db_correction)
        return Confirm(response=True, detail="")
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error: {e}")



@corrections_router.get("/{user}/{oid}", response_model=Confirm)
async def get_is_corrected_user(user: str,oid:str, db: Session = Depends(get_db)):
    """
    Get user history.

    Args:
        user (str): The username.
        db (Session): The database session.

    Returns:
        List[Correction]: A list of Correction objects.
    """
    try:
        correction = db.query(CorrectionSchema).filter(CorrectionSchema.username == user, CorrectionSchema.oid == oid).first()
        if correction is not None:
            return Confirm(response=True, detail="Correction exists.")
        else:
            return Confirm(response=False, detail="Correction does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



@corrections_router.get("/{user}", response_model=List[Correction])
async def get_corrections_user(user: str, db: Session = Depends(get_db)):
    """
    Get user history.

    Args:
        user (str): The username.
        db (Session): The database session.

    Returns:
        List[Correction]: A list of Correction objects.
    """
    try:
        corrections = db.query(CorrectionSchema).filter(CorrectionSchema.username == user).all()
        corrections_models = [Correction(oid=c.oid, username=c.username,pid=c.pid, label=c.label) for c in corrections]
        return corrections_models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")








@corrections_router.post("/comment/", response_model=Confirm)
async def post_comment(comment: Comment, db: Session = Depends(get_db)):
    """
    Post a new comment.

    Args:
        comment (Comment): The Comment object to be posted.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed comment posting.
    """
    try:
        user_db = db.query(UserSchema).filter(UserSchema.username == comment.username).first()
        if user_db is None:
            return Confirm(response=False, detail="User not found")

        db_comment = CommentSchema(user=comment.username, date=comment.date, msg=comment.msg, oid=comment.oid)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return Confirm(response=True, detail="")
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error {e}")




@corrections_router.get("/comment/{oid}", response_model=List[Comment])
async def get_comment(oid: str, db: Session = Depends(get_db)):
    """
    Get comments for a specific object.

    Args:
        oid (str): The object ID.
        db (Session): The database session.

    Returns:
        List[Comment]: A list of Comment objects.
    """
    try:
        comments = db.query(CommentSchema).filter(CommentSchema.oid == oid).all()
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



