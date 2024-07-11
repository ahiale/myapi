from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from app.models.serie import Serie
from app.schemas.serieSchema import SerieCreate, SerieUpdate
from database import get_db
from app.crud.utils import generate_id
import logging


def retriveSerie(serie_id: str, db:Session=Depends(get_db)):
    return db.query(Serie).filter(Serie.id == serie_id).first()

def get_serie(serie_id: str, db:Session=Depends(get_db)):
    serie = db.query(Serie).filter(Serie.id == serie_id).first()
    if not serie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cette serie na pas ete trouve")
    return serie

def create_serie(serie: SerieCreate, db:Session=Depends(get_db)):
    
    rand_id= generate_id()
    while retriveSerie(rand_id, db):
        rand_id=generate_id()
    
    db_serie = Serie(
        id=rand_id,
        titre=serie.titre,
        nb_saisons=serie.nb_saisons,
    )
    
    try:
        db.add(db_serie)
        db.commit()
        db.refresh(db_serie)
        return db_serie    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
       
def update_serie(serie_id: str, serie_update: SerieUpdate, db:Session=Depends(get_db)):
    
    serie = db.query(Serie).filter(Serie.id == serie_id).first()
    
    if not serie:
        raise HTTPException(status_code=404, detail=f"User with ID {serie_id} not found")
    
    serie.titre=serie_update.titre if serie_update.titre else serie.titre
    serie.nb_saisons=serie_update.nb_saisons if serie_update.nb_saisons else serie.nb_saisons
    
    db.commit()
    db.refresh(serie)
    return serie

def delete_serie( serie_id: str, db:Session=Depends(get_db)):
    serie = get_serie(serie_id,db)
    if not serie:
        raise HTTPException(status_code=404, detail=f"User with ID {serie_id} not found")
    db.delete(serie)
    db.commit()
    return True
    
    
def get_all_series(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all series from the database")
        series = db.query(Serie).all()
        logging.info(f"Fetched {len(series)} series")
        return series
    except Exception as e:
        logging.error(f"Error fetching series: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


