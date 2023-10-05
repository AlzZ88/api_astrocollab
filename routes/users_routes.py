from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.comment.comment import Comment
from models.confirm.confirm import Confirm
from models.user.user import User
from schemas.comment_sc.comment_sc import CommentSchema
from schemas.user_sc.user_sc import UserSchema
from data.database_handler import get_db

# Create an APIRouter instance
users_router = APIRouter()



@users_router.get("/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of User objects.
    """
    
    users = db.query(UserSchema).all()
    print(users)
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return users
    




@users_router.post("/", response_model=Confirm)
async def post_user(user: User, db: Session = Depends(get_db)):
    """
    Authenticate a user based on email and password.

    Args:
        user (User): The User object containing email and password.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed login.
    """
    try:
        users = db.query(UserSchema).all()
        
        for u in users:
            if u.mail == user.mail:
                if u.password == user.password:
                    return Confirm(response=True, detail=u.username)
                else:
                    return Confirm(response=False, detail="Incorrect password")
        
        return Confirm(response=False, detail="Incorrect credentials")
    
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error {e}")




@users_router.post("/add", response_model=Confirm)
async def post_user_add(user: User, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (User): The User object to be registered.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed registration.
    """
    try:
        db_user = db.query(UserSchema).filter(UserSchema.mail == user.mail).first()
        if db_user:
            return Confirm(response=False, detail="The mail used already exists")
        
        db_user = db.query(UserSchema).filter(UserSchema.username == user.username).first()
        if db_user:
            return Confirm(response=False, detail="The user already exists")

        new_user = UserSchema(mail=user.mail, username=user.username, password=user.password,privilege=user.privilege)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return Confirm(response=True, detail="")
    except Exception as e:
        return Confirm(response=False, detail=f"Internal server error {e}")

