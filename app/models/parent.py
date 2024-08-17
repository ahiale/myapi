from datetime import datetime, timezone
from sqlalchemy import Column, DateTime,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from ..models.parent_video import parent_video

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(String, primary_key=True)
    nom = Column(String)
    age = Column(Integer)
    motDePasse = Column(String)
    pays = Column(String)
    contact = Column(String,unique=True)
    email = Column(String,unique=True)
    codeParental = Column(String)
    nbre_profil = Column(Integer)
    historique_video = Column(String)
    maxProfilEnfant=Column(Integer, default=5)
    date_inscription = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    # #Relation de plusieurs a un avec enfant
    enfants= relationship("Enfant", back_populates="parent")
    
    videos = relationship(
        "Video",
        secondary=parent_video,
        back_populates="parents"
    )
    
    
