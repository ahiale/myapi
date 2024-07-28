from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from app.models.enfant import Enfant
from app.models.parent import Parent
from app.models import tempsEcran
from app.schemas.enfantSchema import EnfantCreate, EnfantUpdate, EnfantBase 
from app.schemas.tempsEcranSchema import TempsEcranBase
from database import get_db
from app.crud.utils import generate_id
import logging


def retriveEnfant(enfant_id: str, db:Session=Depends(get_db)):
    return db.query(Enfant).filter(Enfant.id == enfant_id).first()

def get_enfant(enfant_id: str, db:Session=Depends(get_db)):
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    if not enfant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet enfant na pas ete trouve")
    return enfant

def create_enfant(enfant: EnfantCreate, db:Session=Depends(get_db)):
         # Vérifie que le parent existe
    parent = db.query(Parent).filter(Parent.id == enfant.parent_id).first()
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet parent nest associe a aucun enfant")
    
    if len(parent.enfants)>= parent.maxProfilEnfant:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Vous ne pouvez creer que 3 profils")
        
    rand_id= generate_id()
    while retriveEnfant(rand_id, db):
        rand_id=generate_id()
    
    db_enfant = Enfant(
        id=rand_id,
        pseudo= enfant.pseudo,
        age=enfant.age,
        image_profil=enfant.image_profil,
        code_pin=enfant.code_pin,
        parent_id=enfant.parent_id
        
        
    )
    
    try:
        db.add(db_enfant)
        db.commit()
        db.refresh(db_enfant)
        return db_enfant    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
    
def get_tempsEcran_by_enfant_id(enfant_id: str, db: Session = Depends(get_db)) -> TempsEcranBase:
    db_enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    if not db_enfant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant non trouvé")
    
    db_tempsEcran = db_enfant.tempsEcrans
    # db_tempsEcran = db.query(TempsEcran).filter(TempsEcran.enfant_id == enfant_id).first()
    if not db_tempsEcran:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temps d'écran non trouvé pour cet enfant")
    
    return db_tempsEcran

    

def update_enfant(enfant_id: str, enfant_update: EnfantUpdate, db:Session=Depends(get_db)):
    
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    
    if not enfant:
        raise HTTPException(status_code=404, detail=f"User with ID {enfant_id} not found")
    
    
    enfant.age=enfant_update.age if enfant_update.age else enfant.age
    enfant.pseudo=enfant_update.pseudo if enfant_update.pseudo else enfant.pseudo
    enfant.image_profil=enfant_update.image_profil if enfant_update.image_profil else enfant.image_profil
    enfant.code_pin=enfant_update.code_pin if enfant_update.code_pin else enfant.code_pin
    
    db.commit()
    db.refresh(enfant)
    return enfant

def delete_enfant( enfant_id: str, db:Session=Depends(get_db)):
    enfant = get_enfant(enfant_id,db)
    if not enfant:
        raise HTTPException(status_code=404, detail=f"User with ID {enfant_id} not found")
    db.delete(enfant)
    db.commit()
    return True
    

# def get_all_enfants(db:Session = Depends(get_db)):
#     return db.query(Enfant).all()
     
#     # return "enfants"
    
    
    

def get_all_enfants(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all enfants from the database")
        enfants = db.query(Enfant).all()
        logging.info(f"Fetched {len(enfants)} enfants")
        return enfants
    except Exception as e:
        logging.error(f"Error fetching enfants: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


