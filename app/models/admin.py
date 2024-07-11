from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(String, primary_key=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    motDePasse = Column(String)
    contact = Column(String,unique=True)
    email = Column(String, unique=True, index=True)
    #Relation de  1 a plusieurs a un
   
    #Relation de 1 a plusieurs avec video 
    videos = relationship("Video", back_populates="admin")
    
  
    

    
    