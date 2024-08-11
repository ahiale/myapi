
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models.enumsVideos import Type_Source_Enum
from database import Base
from app.models.enfant_video import enfant_video  
from app.models.parent_video import parent_video
from app.models.enums import Type_Video_Enum
from app.models.categorie_video import categorie_video  


class Video(Base):

    __tablename__ = 'videos'
    id = Column(String, primary_key=True)
    titre = Column(String)
    description= Column(String)
    duree= Column(String)
    url= Column(String)
    type_Source= Column(Enum(Type_Source_Enum))
    couverture= Column(String)
    type_video= Column(Enum(Type_Video_Enum))
    admin_id=Column(String, ForeignKey("admins.id"), nullable=True)
    saison_id= Column(String, ForeignKey("saisons.id"), nullable=True)
    admin= relationship("Admin", back_populates="videos")
    saison= relationship("Saison", back_populates="videos")
    nbre_like= Column(Integer, default=0)
    categories = relationship(
        "Categorie",
        secondary=categorie_video,
        back_populates="videos",
        lazy='selectin'
    )
    enfants = relationship(
        "Enfant",
        secondary=enfant_video,
        back_populates="videos"
    )
    
    parents = relationship(
        "Parent",
        secondary=parent_video,
        back_populates="videos"
    )

    

    
    



    
    
