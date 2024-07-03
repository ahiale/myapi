from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(String, primary_key=True)
    nom = Column(String)
    age = Column(Integer)
    motDePasse = Column(String)
    pays = Column(String)
    contact = Column(String)
    email = Column(String)
    codeParental = Column(String)
    nbre_profil = Column(Integer)
    historique_video = Column(String)

    admin_id=Column(String, ForeignKey("admins.id"))
    # #Relation de plusieurs a un avec enfant
    enfants= relationship("Enfant", back_populates="parent")
    # #Relation de plusieurs a un avec admin
    admin= relationship("Admin", back_populates="parents")
