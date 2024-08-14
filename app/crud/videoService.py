from cmath import e
import os
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,UploadFile,File
from fastapi.responses import JSONResponse
import requests

from app.models.parent import Parent # type: ignore
# from moviepy.editor import VideoFileClip
from ..models.enumsVideos import Type_Source_Enum
from ..models.video import Video
from ..models.categorie_video import categorie_video

from ..models.admin import Admin
from ..models.saison import Saison
from ..models.enfant_video import enfant_video
from ..models.enfant import Enfant
from ..schemas.videoSchema import VideoCreate, VideoUpdate, VideoBase , LikeResponse
from ..models.enums import Type_Video_Enum
from database import get_db
from ..crud.utils import generate_id
import logging
import httpx
import json
from datetime import datetime
from dotenv import load_dotenv
from ..constants.urls import SERVER_ADDRESS
# import cv2

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_BUCKET = "medias"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}



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

async def create_video(video: VideoCreate, couverture:UploadFile = File(...), db:Session=Depends(get_db)):
    
         # Vérifie que le admin existe
    admin = db.query(Admin).filter(Admin.id == video.admin_id).first()
    # if not admin:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun admin n'est associe a cette video")
    rand_id= generate_id()
    while retriveVideo(rand_id, db):
        rand_id=generate_id()
        
    couv= await upload_image(couverture)
    
    db_video = Video(
        
        id=rand_id,
        titre= video.titre,
        description=video.description,
        duree=video.duree,
        couverture=couv["url"],
        url=str(video.url),
        type_video=Type_Video_Enum(video.type_video),
        type_Source=Type_Source_Enum(video.type_source),
        admin_id=video.admin_id,
        saison_id=video.saison_id, 
        nbre_like=0,  
    )
    
    try:
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        db.execute(categorie_video.insert().values(categorie_id=video.categorie_id, video_id=db_video.id))
        db.commit()
        
        return db_video 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def update_video(video_id: str, video_update: VideoUpdate, db:Session=Depends(get_db)):
    
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail=f"User with ID {video_id} not found")
    try:
        couv=upload_image(video.couverture)
    
        video.titre=video_update.titre if video_update.titre else video.titre
        video.nbre_like=video_update.nbre_like if video_update.nbre_like else video.nbre_like
        # video.couverture=couv["url"] if video_update else video.couverture
        video.description=video_update.description if video_update.description else video.description
        video.url=str(video.url) if str(video.url) else video.url
        video.duree=video_update.duree if video_update.duree else video.duree
        video.type_video=Type_Video_Enum(video.type_video) if Type_Video_Enum(video.type_video) else video.type_video
        video.type_Source=Type_Source_Enum(video.type_Source) if Type_Source_Enum(video.type_Source) else video.type_Source
    
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    

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
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not enfant or not video:
        raise HTTPException(status_code=404, detail="Enfant or Video not found")

    try:
        # Vérifier si l'enfant a déjà un enregistrement pour cette vidéo
        like_entry = db.query(enfant_video).filter(
            enfant_video.c.enfant_id == enfant_id,
            enfant_video.c.video_id == video_id
        ).first()

        if like_entry:
            if like_entry.like:
                # Retirer le like en mettant à jour l'état à False
                db.execute(enfant_video.update().where(
                    enfant_video.c.enfant_id == enfant_id,
                    enfant_video.c.video_id == video_id
                ).values(like=False))
                video.nbre_like-=1
                
            else:
                # Ajouter un like en mettant l'état à True
                db.execute(enfant_video.update().where(
                    enfant_video.c.enfant_id == enfant_id,
                    enfant_video.c.video_id == video_id
                ).values(like=True))
                video.nbre_like+=1

        else:
            # Ajouter un enregistrement de like
            db.execute(enfant_video.insert().values(enfant_id=enfant_id, video_id=video_id, like=True))
        
        db.commit()
        # Récupérer le document dont la variable vient de changer
        updated_like_entry = db.query(enfant_video).filter(
            enfant_video.c.enfant_id == enfant_id,
            enfant_video.c.video_id == video_id
        ).first()
        
        response = LikeResponse(
            enfant_id= updated_like_entry.enfant_id,
            video_id=updated_like_entry.video_id,
            like=updated_like_entry.like
        )

        return response

    except Exception as e:
        db.rollback()  # Annuler les changements en cas d'erreur
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


def retirer_like(enfant_id: str, video_id: str, db: Session):
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
            like_entry.like = False  # Modifier le like pour le marquer comme non-aimé
        else:
            raise HTTPException(status_code=400, detail="Video not liked by this enfant")
    else:
        raise HTTPException(status_code=404, detail="Like entry not found")
    
    db.commit()
    return {"message": "Like removed successfully"}

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
            new_historique=[hist for hist in enfant.historique_video]
            new_historique.append(historique_str)
            enfant.historique_video= new_historique
        logging.info(enfant.historique_video)
        db.commit()
        return True

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  
    
# def readHistorique(enfant_id:str, db: Session = Depends(get_db)):
#     allhistorique=[]
#     enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
#     try:
#         for historique in enfant.historique_video:
#             logging.info(historique)
#             historique_obj=json.loads(historique)
#             video=get_video(historique_obj['video_id'], db)
#             allhistorique.append({
#                 "id": video.id,
#                 "url":video.url,
#                 "description":video.description,
#                 "couverture":video.couverture,
#                 "titre": video.titre,
#                 "date": historique_obj['date'],
                
#             })
#         return allhistorique
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=str(e))  

def readHistorique(enfant_id: str, db: Session = Depends(get_db)):
    historique_dict = {}
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    if enfant is None:
        raise HTTPException(status_code=404, detail="Enfant not found")
    
    try:
        for historique in enfant.historique_video:
            historique_obj = json.loads(historique)
            video = db.query(Video).filter(Video.id == historique_obj["video_id"]).first()
            
            if video:
                video_id = video.id
            
                if video_id not in historique_dict or historique_obj['date'] > historique_dict[video_id]['date']:
                    historique_dict[video_id] = {
                        "id": video.id,
                        "url": video.url,
                        "description": video.description,
                        "couverture": video.couverture,
                        "titre": video.titre,
                        "date": historique_obj['date']
                    }
            
        allhistorique = list(historique_dict.values())
        return allhistorique
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    
# methode pour upload une video
async def generate_signed_url(file_name: str, expires_in: int):
    url = f"{SUPABASE_URL}/storage/v1/object/sign/{SUPABASE_BUCKET}/{file_name}?expiresIn={expires_in}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, timeout=30.0)  # Timeout de 30 secondes
        if response.status_code == 200:
            return response.json().get('signedURL')
        else:
            print(f"Failed to generate signed URL: {response.status_code} - {response.text}")
            return None

async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    file_name = file.filename

    try:
        with open("media/videos/"+file_name, 'wb') as f:
            f.write(file_content)
        return {"message": "File uploaded successfully","url":f"http://{SERVER_ADDRESS}/videos/{file_name}"}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

async def upload_image(file: UploadFile = File(...)):
    file_content = await file.read()
    file_name = file.filename

    try:
        with open("media/couvertures/"+file_name, 'wb') as f:
            f.write(file_content)
        return {"message": "File uploaded successfully","url":f"http://{SERVER_ADDRESS}/images/{file_name}"}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
        
def get_like_status(db: Session, video_id: str, enfant_id: str):
    
    
     # Récupérer l'enfant et la vidéo correspondants à partir de la base de données
    enfant = db.query(Enfant).filter(Enfant.id == enfant_id).first()
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not enfant or not video:
        raise HTTPException(status_code=404, detail="Enfant or Video not found")

    try:
        # Vérifier si l'enfant a déjà un enregistrement pour cette vidéo
        like_entry = db.query(enfant_video).filter(
            enfant_video.c.enfant_id == enfant_id,
            enfant_video.c.video_id == video_id
        ).first()
        if(like_entry):
            return {"liked":like_entry.like}
        return HTTPException(status_code=404, detail="Video or Enfant not found") 
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))   


def remove_video_from_lists(db: Session, video_id: str, parent_id: str):
    try:
        # Retirer la vidéo de la liste du parent
        parent = db.query(Parent).filter(Parent.id == parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent non trouvé")
        parent.videos = [video for video in parent.videos if video.id != video_id]
        db.add(parent)
        
        # Retirer la vidéo de la liste des enfants du parent
        enfants = db.query(Enfant).filter(Enfant.parent_id == parent_id).all()
        for enfant in enfants:
            enfant.videos = [video for video in enfant.videos if video.id != video_id]
            db.add(enfant)
        
        db.commit()
        return {"message": "Vidéo retirée des listes"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour des listes")    
   