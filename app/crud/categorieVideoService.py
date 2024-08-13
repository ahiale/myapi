from fastapi import HTTPException, status,Depends
from sqlalchemy.orm import Session
from ..crud.categorieService import get_categorie
from ..crud.utils import generate_id
from ..crud.videoService import get_video
from ..models.categorie_video import categorie_video
from ..models.categorie import Categorie
from ..models.video import Video
from database import get_db
from ..schemas.categorieVideoSchema import CategorieVideoCreate
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder


def retrive_categorie_videos(db:Session=Depends(get_db)):
    # return db.query(categorie_video).all
    req = select(categorie_video)
    results = db.execute(req).fetchall()
    results_json = [
            {"categorie_id": row[0], "video_id": row[1]}
            for row in results
        ]
    return results_json

def retrive_categorie_by_video_id(video_id:str,db:Session=Depends(get_db)):
    # Construire la requête
    stmt = select(categorie_video).where(categorie_video.c.video_id == video_id)
    
    # Exécuter la requête et obtenir les résultats
    results = db.execute(stmt).fetchall()
    
    # Convertir les résultats en une liste de dictionnaires
    results_json = [
        {"categorie_id": row.categorie_id}
        for row in results
    ]
    
    return results_json

def retrive_videos_by_categorie_id(categorie_id: str, db:Session=Depends(get_db)):
    # Construire la requête
    stmt = select(categorie_video).where(categorie_video.c.categorie_id == categorie_id)
    
    # Exécuter la requête et obtenir les résultats
    results = db.execute(stmt).fetchall()
    
    # Convertir les résultats en une liste de dictionnaires
    video_ids = [
        row.video_id
        for row in results
    ]
    categorie_infos = get_categorie(categorie_id, db)
     # Obtenir les informations des vidéos pour chaque ID
    videos_info = []
    videos_info.append(categorie_infos)
    for vid in video_ids:
        video_info = get_video(vid, db)
        if video_info:
            videos_info.append(video_info)
    
    return videos_info

def create_categorie_video(cat_vid: CategorieVideoCreate , db:Session=Depends(get_db)):
    
    # rand_id= generate_id()
    # while retriveCategorieVideo(rand_id, db):
    #     rand_id=generate_id()
        
    # hashed_password = hash_password(admin.motDePasse)
    
    db_categorie_video = categorie_video(
       categorie_id = cat_vid.categorie_id,
       video_id = cat_vid.video_id  
    )
    
    try:
        db.add(db_categorie_video)
        db.commit()
        db.refresh(db_categorie_video)
        return db_categorie_video    
    except Exception as e:
        raise HTTPException(status_code=500, detail="International server error")
    