from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from data.database_handler import Base

class CommentSchema(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), ForeignKey('users.username'))
    date = Column(String(255))
    msg = Column(Text)
    oid = Column(String(50))
    user = relationship('UserSchema', back_populates='comments')
    def __str__(self):
        return f"Comment(id={self.id}, user={self.user}, date={self.date}, msg={self.msg}, oid={self.oid})"