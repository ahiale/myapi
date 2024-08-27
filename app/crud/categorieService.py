from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from ..models.categorie import Categorie
from ..schemas.categorieSchema import CategorieCreate, CategorieUpdate
from database import get_db
from ..crud.utils import generate_id
import logging

def retriveCategorie(categorie_id: str, db:Session=Depends(get_db)):
    return db.query(Categorie).filter(Categorie.id == categorie_id).first()

def get_categorie(categorie_id: str, db:Session=Depends(get_db)):
    categorie = db.query(Categorie).filter(Categorie.id == categorie_id).first()
    if not categorie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cette categorie na pas ete trouve")
    return categorie

def create_categorie(categorie: CategorieCreate, db:Session=Depends(get_db)):
    
    rand_id= generate_id()
    while retriveCategorie(rand_id, db):
        rand_id=generate_id()
    
    db_categorie = Categorie(
        id=rand_id,
        titre=categorie.titre,
    )
    
    try:
        db.add(db_categorie)
        db.commit()
        db.refresh(db_categorie)
        return db_categorie    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
       
def update_categorie(categorie_id: str, categorie_update: CategorieUpdate, db:Session=Depends(get_db)):
    
    categorie = db.query(Categorie).filter(Categorie.id == categorie_id).first()
    
    if not categorie:
        raise HTTPException(status_code=404, detail=f"User with ID {categorie_id} not found")
    
    categorie.titre=categorie_update.titre if categorie_update.titre else categorie.titre
    
    db.commit()
    db.refresh(categorie)
    return categorie

def delete_categorie( categorie_id: str, db:Session=Depends(get_db)):
    categorie = get_categorie(categorie_id,db)
    if not categorie:
        raise HTTPException(status_code=404, detail=f"User with ID {categorie_id} not found")
    db.delete(categorie)
    db.commit()
    return True
    
def get_all_categories(parent_id:str|None=None,db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all categories from the database")
        categories = db.query(Categorie).all()
        if parent_id is not None:
            query = f"""
            SELECT video_id
            FROM parent_video
            WHERE parent_id = '{parent_id}'
            AND interested = true
            """
              # Define the SQL statement using text()
            stmt = text(query)
                # Execute the query
            res = db.execute(stmt)
            videocategorie_ids = [i[0] for i in res.fetchall()]
            logging.error(videocategorie_ids)
            for categorie in categories:
                tempVideos=categorie.videos
                categorie.videos=[video for video in  tempVideos if video.id not in videocategorie_ids]
        logging.info(f"Fetched {len(categories)} categories")
        return categories
    except Exception as e:
        logging.error(f"Error fetching categories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


