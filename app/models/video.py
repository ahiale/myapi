
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from app.models.enfant_video import enfant_video  # Import de la table de liaison
from app.models.parent_video import parent_video
from app.models.enums import Type_Video_Enum
from app.models.categorie_video import categorie_video  # Import de la table de liaison

class Video(Base):

    __tablename__ = 'videos'
    id = Column(String, primary_key=True)
    titre = Column(String)
    description= Column(String)
    duree= Column(String)
    url= Column(String)
    type_video= Column(Enum(Type_Video_Enum))
    
    admin_id=Column(String, ForeignKey("admins.id"), nullable=True)
    saison_id= Column(String, ForeignKey("saisons.id"), nullable=True)
    #Relation plusieurs a un avec admin
    admin= relationship("Admin", back_populates="videos")
    #Relation plusieurs a un avec saison
    saison= relationship("Saison", back_populates="videos")
    
    categories = relationship(
        "Categorie",
        secondary=categorie_video,
        back_populates="videos"
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

    

    
    



    
    
