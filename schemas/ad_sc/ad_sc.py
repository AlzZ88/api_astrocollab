from sqlalchemy import Column, Integer, String,Text
from data.database_handler import Base
class AdSchema(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(140))
    img = Column(Text)
