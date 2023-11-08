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


@corrections_router.get("/corrected/{pid}/{username}", response_model=List[str])
async def get_corrections_by_username_and_pid(username: str, pid: int, db: Session = Depends(get_db)):
    db_corrections = db.query(CorrectionSchema).filter(CorrectionSchema.username == username, CorrectionSchema.pid == pid).all()
    if not db_corrections:
        raise HTTPException(status_code=404, detail="Corrections not found for the given username and pid")

    oid_list = [correction.oid for  correction in db_corrections]
    return oid_list

@corrections_router.get("/noncorrected/{pid}/{username}", response_model=List[str])
async def get_corrections_by_username_and_pid(username: str, pid: int, db: Session = Depends(get_db)):
    db_corrections = db.query(CorrectionSchema).filter(CorrectionSchema.pid == pid, CorrectionSchema.username != username).all()

    if not db_corrections:
        raise HTTPException(status_code=404, detail="Corrections not found for the given username and pid")

    oid_list = [correction.oid for  correction in db_corrections]
    return oid_list

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


@corrections_router.get("/comment/", response_model=List[Comment])
async def get_comments(db: Session = Depends(get_db)):
    """
    Get user history.

    Args:
        user (str): The username.
        db (Session): The database session.

    Returns:
        List[HistoryItem]: A list of HistoryItem objects.
    """
    db_history = db.query(CommentSchema).all()
    if not db_history:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_history



@corrections_router.post("/", response_model=Confirm)
async def post_object_correction(correction: Correction, db: Session = Depends(get_db)):
    
    """ Post object correction.

    Args:
        correction (Correction): The Correction object containing object and project ID, the username and correction.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed correction posting. """
    existing_correction = db.query(CorrectionSchema).filter(
        CorrectionSchema.username == correction.username,
        CorrectionSchema.oid == correction.oid
    ).first()
    print(existing_correction)
    if existing_correction is not None:
        existing_correction.label = correction.label
        db.commit()
        db.refresh(existing_correction)
        return Confirm(response=True, detail="Correction updated.",user=User(privilege=False,mail="",username="",password=""))

    
    else:
        db_correction = CorrectionSchema(
            oid=correction.oid,
            username=correction.username,
            pid=correction.pid,
            label=correction.label
        )
        db.add(db_correction)
        db.commit()
        db.refresh(db_correction)
        return Confirm(response=True, detail="Correction inserted.",user=User(privilege=False,mail="",username="",password=""))




@corrections_router.post("/exits/", response_model=Confirm)
async def post_is_corrected_user(correction: Correction, db: Session = Depends(get_db)):
    """
    Get user history.

    Args:
        user (str): The username.
        db (Session): The database session.

    Returns:
        List[Correction]: A list of Correction objects.
    """
    try:
        correction = db.query(CorrectionSchema).filter(CorrectionSchema.username == correction.username, CorrectionSchema.oid == correction.oid).first()
        if correction is not None:
            return Confirm(response=True, detail="Correction exists.",user=User(privilege=False,mail="",username="",password=""))

        else:
            return Confirm(response=False, detail="Correction does not exist.",user=User(privilege=False,mail="",username="",password=""))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}",user=User(privilege=False,mail="",username="",password=""))




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
            return Confirm(response=False, detail="User not found",user=User(privilege=False,mail="",username="",password=""))

        db_comment = CommentSchema(username=comment.username, date=comment.date, msg=comment.msg, oid=comment.oid)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return Confirm(response=True, detail="",user=User(privilege=user_db.privilege,mail=user_db.mail,username=user_db.username,password=user_db.password))
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error {e}",user=User(privilege=False,mail="",username="",password=""))





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
   
    comments = db.query(CommentSchema).filter(CommentSchema.oid == oid).all()
    print(comments)
    if not comments:
        raise HTTPException(status_code=404, detail="Comments not found")
    return comments
    


