from sqlalchemy import Column, String, Integer, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from ..models.enfant_video import enfant_video  # Import de la table de liaison

class Enfant(Base):
    __tablename__ = 'enfants'

    id = Column(String, primary_key=True)
    pseudo = Column(String)
    image_profil = Column(String)
    age = Column(Integer)
    code_pin = Column(String)
    historique_video = Column(ARRAY(String))
    parent_id= Column(String, ForeignKey("parents.id"))
    # #Relation de plusieurs a un avec parent
    parent= relationship("Parent", back_populates="enfants")
    
     # #Relation de un a un avec tempsEcran
    videos = relationship(
        "Video",
        secondary=enfant_video,
        back_populates="enfants"
    )
    #Relation de plusieurs a un avec TempsEcran
    tempsEcrans= relationship("TempsEcran", back_populates="enfant")
    

   
    
    
    
