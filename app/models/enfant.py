from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, ARRAY
from database import Base
from sqlalchemy.orm import relationship
# from app.models.video import Video
from app.models.enfant_video import enfant_video  # Forward reference

 


class Enfant(Base):
    __tablename__ = 'enfants'

    id = Column(String, primary_key=True)
    pseudo = Column(String)
    image_profil = Column(String)
    age = Column(Integer)
    allocation = Column(String)
    joursA = Column(ARRAY(String))
    heuresA = Column(ARRAY(String))
    code_pin = Column(String)
    historique_video = Column(ARRAY(String))
    parent_id= Column(String, ForeignKey("parents.id"))
    # #Relation de plusieurs a un avec parent
    parent= relationship("Parent", back_populates="enfants")
    
    videos = relationship(
        "Video",
        secondary=enfant_video,
        back_populates="enfants"
    )

    # # # Many-to-many relationship with Video
    # videos = relationship(
    #      "Video",
    #      secondary=enfant_video,
    #      back_populates="enfants"
    #  )
    
    
    
