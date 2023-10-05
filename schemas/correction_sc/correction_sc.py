from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.database_handler import Base
# Define el modelo para la tabla 'corrections'
class CorrectionSchema(Base):
    __tablename__ = 'corrections'

    oid = Column(String(50), primary_key=True)
    username = Column(String(30), ForeignKey('users.username'))  # Clave externa que hace referencia a 'users.username'
    label = Column(String(50))
    pid = Column(Integer, ForeignKey('projects.pid'))  # Clave externa que hace referencia a 'projects.pid'
    
    # Relaciones con las tablas relacionadas
    project = relationship('ProjectSchema', backref='corrections_project')
    user = relationship('UserSchema', backref='corrections_user')


    
    def __str__(self):
        return f"Correction(id={self.id}, user={self.user}, label={self.label}, oid={self.oid}, pid={self.pid})"