from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from ..models.saison import Saison
from ..schemas.saisonSchema import SaisonCreate, SaisonUpdate
from database import get_db
from ..crud.utils import generate_id
import logging


def retriveSaison(saison_id: str, db:Session=Depends(get_db)):
    return db.query(Saison).filter(Saison.id == saison_id).first()

def get_saison(saison_id: str, db:Session=Depends(get_db)):
    saison = db.query(Saison).filter(Saison.id == saison_id).first()
    if not saison:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cette saison na pas ete trouve")
    return saison

def create_saison(saison: SaisonCreate, db:Session=Depends(get_db)):
    
    rand_id= generate_id()
    while retriveSaison(rand_id, db):
        rand_id=generate_id()
    
    db_saison = Saison(
        id=rand_id,
        titre=saison.titre,
        nb_episodes=saison.nb_episodes,
        serie_id=saison.serie_id,
    )
    
    try:
        db.add(db_saison)
        db.commit()
        db.refresh(db_saison)
        return db_saison    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
       
def update_saison(saison_id: str, saison_update: SaisonUpdate, db:Session=Depends(get_db)):
    
    saison = db.query(Saison).filter(Saison.id == saison_id).first()
    
    if not saison:
        raise HTTPException(status_code=404, detail=f"User with ID {saison_id} not found")
    
    saison.titre=saison_update.titre if saison_update.titre else saison.titre
    saison.nb_episodes=saison_update.nb_episodes if saison_update.nb_episodes else saison.nb_episodes
    
    db.commit()
    db.refresh(saison)
    return saison

def delete_saison( saison_id: str, db:Session=Depends(get_db)):
    saison = get_saison(saison_id,db)
    if not saison:
        raise HTTPException(status_code=404, detail=f"User with ID {saison_id} not found")
    db.delete(saison)
    db.commit()
    return True
    
    

def get_all_saisons(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all saisons from the database")
        saisons = db.query(Saison).all()
        logging.info(f"Fetched {len(saisons)} saisons")
        return saisons
    except Exception as e:
        logging.error(f"Error fetching saisons: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


