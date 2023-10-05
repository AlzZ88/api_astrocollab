from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship
from data.database_handler import Base

class UserSchema(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mail = Column(String(100), unique=True)
    username = Column(String(30), unique=True)
    password = Column(String(15))
    privilege = Column(Boolean)
    comments = relationship('CommentSchema', back_populates='user')
    #corrections = relationship('CorrectionSchema', back_populates='user')