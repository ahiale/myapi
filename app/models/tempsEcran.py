from sqlalchemy import Column, String, Integer, ForeignKey, Table,Time
from database import Base, metadata
# from app.models.categorie_video import Categorie_video
from sqlalchemy.orm import relationship

class TempsEcran(Base):
    __tablename__ = 'tempsEcrans'
    id = Column(String, primary_key=True)
    joursA= Column(String)
    heuresD=Column(Time)
    heuresF=Column(Time)
    
#Relation de plusieurs a un avec enfants
    enfant_id= Column(String, ForeignKey("enfants.id"))
    enfant= relationship("Enfant", back_populates="tempsEcrans")
