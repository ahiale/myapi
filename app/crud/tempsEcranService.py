from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from ..models.tempsEcran import TempsEcran
from ..models.enfant import Enfant
from ..schemas.tempsEcranSchema import TempsEcranCreate, TempsEcranUpdate, TempsEcranBase 
from database import get_db
from ..crud.utils import generate_id
import logging


def retriveTempsEcran(tempsEcran_id: str, db:Session=Depends(get_db)):
    return db.query(TempsEcran).filter(TempsEcran.id == tempsEcran_id).first()

def get_tempsEcran(tempsEcran_id: str, db:Session=Depends(get_db)):
    tempsEcran = db.query(TempsEcran).filter(TempsEcran.id == tempsEcran_id).first()
    if not tempsEcran:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet tempsEcran na pas ete trouve")
    return tempsEcran

def get_enfant_id_by_temps_ecran_id(tempsEcran_id: str, db: Session = Depends(get_db)):
    db_tempsEcran = db.query(TempsEcran).filter(TempsEcran.id == tempsEcran_id).first()
    if not db_tempsEcran:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temps d'écran non trouvé")
    
    enfant_id = db_tempsEcran.enfant_id
    if not enfant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant non trouvé pour ce temps d'écran")
    
    return  enfant_id

def create_tempsEcran(tempsEcran: TempsEcranCreate, db:Session=Depends(get_db)):
         # Vérifie que le enfant existe
    enfant = db.query(Enfant).filter(Enfant.id == tempsEcran.enfant_id).first()
    if not enfant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet temps decran n'est associe a aucun enfant")
        
    rand_id= generate_id()
    while retriveTempsEcran(rand_id, db):
        rand_id=generate_id()
    
    db_tempsEcran = TempsEcran(
        id=rand_id,
        heuresD=tempsEcran.heuresD,
        heuresF=tempsEcran.heuresF,
        joursA=tempsEcran.joursA,
        enfant_id=tempsEcran.enfant_id,   
    )
    
    try:
        db.add(db_tempsEcran)
        db.commit()
        db.refresh(db_tempsEcran)
        return db_tempsEcran    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
    

def update_tempsEcran(tempsEcran_id: str, tempsEcran_update: TempsEcranUpdate, db:Session=Depends(get_db)):
    
    tempsEcran = db.query(TempsEcran).filter(TempsEcran.id == tempsEcran_id).first()
    
    if not tempsEcran:
        raise HTTPException(status_code=404, detail=f"User with ID {tempsEcran_id} not found")
    
    try:
    
        tempsEcran.heuresD=tempsEcran_update.heuresD if tempsEcran_update.heuresD else tempsEcran.heuresD
        tempsEcran.heuresF=tempsEcran_update.heuresF if tempsEcran_update.heuresF else tempsEcran.heuresF
        tempsEcran.joursA=tempsEcran_update.joursA if tempsEcran_update.joursA else tempsEcran.joursA
    
        db.commit()
        db.refresh(tempsEcran)
        return tempsEcran
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="International server error")
    

def delete_tempsEcran( tempsEcran_id: str, db:Session=Depends(get_db)):
    tempsEcran = get_tempsEcran(tempsEcran_id,db)
    if not tempsEcran:
        raise HTTPException(status_code=404, detail=f"User with ID {tempsEcran_id} not found")
    db.delete(tempsEcran)
    db.commit()
    return True
    

def get_all_tempsEcrans(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all tempsEcrans from the database")
        tempsEcrans = db.query(TempsEcran).all()
        logging.info(f"Fetched {len(tempsEcrans)} tempsEcrans")
        return tempsEcrans
    except Exception as e:
        logging.error(f"Error fetching tempsEcrans: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


