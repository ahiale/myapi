from sqlalchemy import Column,String,Integer,Boolean, ForeignKey,Time
from database import Base
from sqlalchemy.orm import relationship

class Serie(Base):
    __tablename__ = 'series'

    id = Column(String, primary_key=True)
    titre = Column(String)
    description = Column(String)
    nb_saisons = Column(Integer)
    # #Relation de un à plusieurs avec saisons
    saisons = relationship("Saison", back_populates="serie")

   


