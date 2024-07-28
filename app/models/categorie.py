from sqlalchemy import Column, String, Integer, ForeignKey, Table
from database import Base, metadata
# from app.models.categorie_video import Categorie_video
from sqlalchemy.orm import relationship
from app.models.categorie_video import categorie_video




class Categorie(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    titre = Column(String)
    
    
    
    videos = relationship(
        'Video',
        secondary=categorie_video,
        back_populates='categories',
        lazy='selectin'
    )
    
    
