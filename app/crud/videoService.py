from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from app.models.video import Video
from app.models.admin import Admin
from app.models.saison import Saison
from app.models.enfant_video import enfant_video
from app.models.enfant import Enfant
from app.schemas.videoSchema import VideoCreate, VideoUpdate, VideoBase 
from app.models.enums import Type_Video_Enum
from database import get_db
from app.crud.utils import generate_id
import logging
import json
from datetime import datetime



def retriveVideo(video_id: str, db:Session=Depends(get_db)):
    return db.query(Video).filter(Video.id == video_id).first()

def get_video(video_id: str, db:Session=Depends(get_db)):
    
    video = db.query(Video).filter(Video.id == video_id).first()
    try:
        if not video:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cette video na pas ete trouve")
        return video
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def create_video(video: VideoCreate, db:Session=Depends(get_db)):
         # Vérifie que le admin existe
    admin = db.query(Admin).filter(Admin.id == video.admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun admin n'est associe a cette video")
   
    rand_id= generate_id()
    while retriveVideo(rand_id, db):
        rand_id=generate_id()
    
    db_video = Video(
        id=rand_id,
        titre= video.titre,
        description=video.description,
        duree=video.duree,
        url=str(video.url),
        type_video=Type_Video_Enum(video.type_video),
        admin_id=video.admin_id,
        saison_id=video.saison_id,
        
    )
    
    try:
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def update_video(video_id: str, video_update: VideoUpdate, db:Session=Depends(get_db)):
    
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail=f"User with ID {video_id} not found")
    
    
    video.titre=video_update.titre if video_update.titre else video.titre
    video.description=video_update.description if video_update.description else video.description
    video.url=str(video.url) if str(video.url) else video.url
    video.duree=video_update.duree if video_update.duree else video.duree
    video.type_video=Type_Video_Enum(video.type_video) if Type_Video_Enum(video.type_video) else video.type_video
    
    db.commit()
    db.refresh(video)
    return video

def delete_video( video_id: str, db:Session=Depends(get_db)):
    video = get_video(video_id,db)
    if not video:
        raise HTTPException(status_code=404, detail=f"User with ID {video_id} not found")
    db.delete(video)
    db.commit()
    return True
    

def get_all_videos(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all videos from the database")
        videos = db.query(Video).all()
        logging.info(f"Fetched {len(videos)} videos")
        return videos
    except Exception as e:
        logging.error(f"Error fetching videos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

def liker_video(enfant_id: str, video_id: str, db: Session):
    # Récupérer l'enfant et la vidéo correspondants à partir de la base de données
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    video = get_video(video_id, db)
    
    if not enfant or not video:
        raise HTTPException(status_code=404, detail="Enfant or Video not found")
    
    # Vérifier si l'enfant a déjà liké cette vidéo
    like_entry = db.query(enfant_video).filter(
        enfant_video.c.enfant_id == enfant_id,
        enfant_video.c.video_id == video_id
    ).first()

    if like_entry:

        if like_entry.like:
            raise HTTPException(status_code=400, detail="Video already liked by this enfant")
        else:
            
            like_entry.like = True
    else:
       
        db.execute(enfant_video.insert().values(enfant_id=enfant_id, video_id=video_id, like=True))
    

    db.commit()
    return True

# Gestion de historique video

def consulter_video(enfant_id: str, video_id: str, db: Session = Depends(get_db)):
    
    date_actuelle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    video = get_video(video_id, db)
    
    
    if not enfant or not video:
        raise HTTPException(status_code=404, detail="Enfant or Video not found")
    
    try:
        historique = {
        'video_id': video_id,
        'date': date_actuelle
        }
        historique_str = json.dumps(historique)
        
        if enfant.historique_video is None:
            enfant.historique_video=[historique_str]
        else:
            enfant.historique_video.append(historique_str)
    
        db.commit()
        db.refresh(enfant)
        return True

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  
    
def readHistorique(enfant_id:str, db: Session = Depends(get_db)):
    allhistorique=[]
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    try:
        for historique in enfant.historique_video:
            logging.info(historique)
            historique_obj=json.loads(historique)
            video=get_video(historique_obj['video_id'], db)
            allhistorique.append({
                "titre": video.titre,
                "date": historique_obj['date'],
                
            })
        return allhistorique
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  

   