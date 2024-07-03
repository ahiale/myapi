from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Saison(Base):
    __tablename__ = 'saisons'

    id = Column(String, primary_key=True)
    titre = Column(String)
    nb_episodes = Column(Integer)
    
    serie_id= Column(String, ForeignKey("series.id"))
    # #Relation de un à plusieurs avec videos
    videos = relationship("Video", back_populates="saison")
    # #Relation de  plusieurs a un avec serie
    serie= relationship("Serie", back_populates="saisons")

