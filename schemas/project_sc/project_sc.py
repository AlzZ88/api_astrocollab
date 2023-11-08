from sqlalchemy import Column, Integer, String, ARRAY, JSON
from data.database_handler import Base

# Define el modelo para la tabla 'projects'
class ProjectSchema(Base):
    __tablename__ = 'projects'
    pid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(500))
    labels = Column(JSON)
    objects = Column(JSON)
    
    def __str__(self):
        return f"ProjectSchema(name={self.name}, description={self.description}, labels={self.labels}, objects={self.objects})"