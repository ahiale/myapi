import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Form, HTTPException, status,Depends,APIRouter,Query, UploadFile, File
from ..models.video import Video
from ..models.parent import Parent
from typing import List
# from schemas.videoSchema import VideoCreate, VideoUpdate 
from database import get_db
from ..crud.videoService import get_like_status, get_video, get_all_videos, create_video, remove_video_from_lists, update_video, delete_video, liker_video, consulter_video,readHistorique, upload_file, retirer_like
from ..crud.utils import generate_id
from ..schemas.videoSchema import TypeSourceEnum, TypeVideoEnum, VideoCreate,VideoUpdate, SearchCriteria, VideoBase
from ..models.parent_video import parent_video
from fastapi.responses import FileResponse
from sqlalchemy.sql import select
from sqlalchemy.engine import Connection
from sqlalchemy import create_engine, desc, insert, update
# from fastapi.responses import JSONResponse
# from app.models.categorie_video import CategorieVideo

video_folder = "media/videos/"

router=APIRouter()

@router.get("/allVideo")
def readU(db: Session=Depends(get_db)):
    videos=get_all_videos(db)
    if not videos:
        raise HTTPException(status_code=404, detail="No video found")
    return videos

# GET /video/{video_id}
@router.get("/{video_id}")
def read_video_controller(video_id: str, db: Session = Depends(get_db)):
    try:
        video = get_video(video_id, db)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /video/
@router.post("/createVideo")
async def create_video_controller(titre:str= Form(...),description : str=Form(...),duree:str=Form(...),type_video:int=Form(...),video_source:int=Form(...),url: str=Form(...),saison_id:str=None,categorie_id:str=Form(...), couverture:UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        video = await create_video(VideoCreate(
            titre=titre,
            description = description,
            duree=duree,
            type_video=TypeVideoEnum(type_video),
            type_source=TypeSourceEnum(video_source),
            url=url,
            saison_id=saison_id,
            nbre_like=0,
            categorie_id=categorie_id),couverture, db)
        return video,status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#PUT /video/{video_id}
@router.put("/edit/{video_id}")
def update_video_controller(video_id: str, video: VideoUpdate, db: Session = Depends(get_db)):
    
    try:
        video = update_video(video_id, video, db)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video,status.HTTP_200_OK
    except Exception as e:
        logging.info(video)
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /video/{video_id}
@router.delete("/delete/{video_id}")
def delete_video_controller(video_id: str, db: Session = Depends(get_db)):
    try:
        video = get_video(video_id, db)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        response = delete_video(video_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete video")
        return {"message": "Video deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/{video_id}/{enfant_id}/like")
def like_video(video_id: str, enfant_id: str, db: Session = Depends(get_db)):
    try:
        # Appeler la fonction pour gérer l'ajout ou la suppression du like
        res = liker_video(enfant_id, video_id, db)
        return res
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/{video_id}/{enfant_id}/consulter")
def consulter_video_endpoint(video_id: str, enfant_id: str, db: Session = Depends(get_db)):
    try:
        consulter_video(enfant_id, video_id, db)
        return {"message": "Video consulted successfully"}, status.HTTP_200_OK
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lire/{enfant_id}")
def lire_historique_endpoint( enfant_id: str, db: Session = Depends(get_db)):
    try:
        return readHistorique(enfant_id, db)   
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="lecture impossible ")
    
@router.get("/search/")
def search_videos(criteria: SearchCriteria = Depends(), db: Session = Depends(get_db)):
    videos = db.query(Video).filter(
        Video.titre.like("%"+ criteria.query+ "%") | Video.description.like("%"+ criteria.query+ "%")
        )
    return videos.all()

@router.post("/upload/")
async def upload(file: UploadFile = File(...)):
    response = await upload_file(file)
    return JSONResponse(content=response)


@router.get("/media/video/{video_name}")
async def readVideo(video_name: str):
    path = f"{video_folder}{video_name}"
    return FileResponse(path)


    
@router.get("/video/{video_id}/{enfant_id}/like_status")
def get_like_status_route(video_id: str, enfant_id: str, db: Session = Depends(get_db)):
    try:
        # Appeler la méthode pour obtenir l'état du like
        result = get_like_status(db, video_id, enfant_id)
        
        # Si le résultat contient un message d'erreur, lever une exception HTTP
        if "detail" in result:
            raise HTTPException(status_code=404, detail=result["detail"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/top-liked-videos")
# def get_top_liked_videos(db: Session = Depends(get_db)):
#     """Retourne les vidéos les plus aimées, jusqu'à un maximum de 10 vidéos, ou un tableau vide si aucune vidéo n'a été aimée."""
#     query = select(Video).filter(Video.nbre_like > 0).order_by(desc(Video.nbre_like)).limit(10)
#     videos = db.execute(query).scalars().all()
#     return [
#         {
#             "titre": video.titre,
#             "nbre_like": video.nbre_like
#         }
#         for video in videos
#     ]


@router.post("/update-interest/{parent_id}/{video_id}/{interested}/{motif}")
def update_interest(parent_id: str, video_id: str, interested: bool, motif: str = None, db: Session = Depends(get_db)):
    # Récupérer le parent et la vidéo correspondants à partir de la base de données
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not parent or not video:
        raise HTTPException(status_code=404, detail="Parent or Video not found")
    
    try:
        # Vérifier si le parent a déjà un enregistrement pour cette vidéo
        existing_entry = db.query(parent_video).filter(
            parent_video.c.parent_id == parent_id,
            parent_video.c.video_id == video_id
        ).first()
        
        if existing_entry:
            if interested:
                # Mettre à jour l'état d'intérêt et le motif
                db.execute(
                    update(parent_video)
                    .where(parent_video.c.parent_id == parent_id)
                    .where(parent_video.c.video_id == video_id)
                    .values(interested=True, motifs=motif)
                )
            else:
                # Mettre à jour l'état d'intérêt et supprimer le motif
                db.execute(
                    update(parent_video)
                    .where(parent_video.c.parent_id == parent_id)
                    .where(parent_video.c.video_id == video_id)
                    .values(interested=False, motifs=None)
                )
        
        else:
            # Ajouter un nouvel enregistrement
            db.execute(
                insert(parent_video).values(
                    parent_id=parent_id,
                    video_id=video_id,
                    interested=interested,
                    motifs=motif if interested else None
                )
            )

        db.commit()

        # Récupérer le document dont la variable vient de changer
        updated_entry = db.query(parent_video).filter(
            parent_video.c.parent_id == parent_id,
            parent_video.c.video_id == video_id
        ).first()

        response = {
            "parent_id": updated_entry.parent_id,
            "video_id": updated_entry.video_id,
            "interested": updated_entry.interested,
            "motifs": updated_entry.motifs
        }

        return response
    
    except Exception as e:
        db.rollback()  # Annuler les changements en cas d'erreur
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/get-all-motifs/")
def get_all_motifs(db: Session = Depends(get_db)):
    try:
        # Requête pour récupérer le nom du parent, le titre de la vidéo, et le motif
        query = (
            db.query(Parent.nom.label("nom"),Parent.id.label("parent_id"), Video.id.label("video_id"),Video.titre.label("titre"), parent_video.c.motifs)
            .join(parent_video, Parent.id == parent_video.c.parent_id)
            .join(Video, Video.id == parent_video.c.video_id)
            .filter(parent_video.c.motifs.isnot(None))  # Filtrer pour ne récupérer que les entrées avec des motifs
            .all()
        )

        # Préparer la réponse
        response = []
        for result in query:
            response.append({
                "parent_id":result.parent_id,
                "video_id":result.video_id,
                "nom": result.nom,
                "titre": result.titre,
                "motif": result.motifs
            })

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.delete("/video/remove-from-lists/{video_id}/{parent_id}")
async def remove_video_from_lists_route(video_id: str, parent_id: str, db: Session = Depends(get_db)):
    return remove_video_from_lists(db, video_id, parent_id)