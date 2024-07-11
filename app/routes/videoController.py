from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.video import Video
from app.models.parent import Parent
# from schemas.videoSchema import VideoCreate, VideoUpdate 
from database import get_db
from app.crud.videoService import get_video, get_all_videos, create_video, update_video, delete_video, liker_video, consulter_video,readHistorique
from app.crud.utils import generate_id
from app.schemas.videoSchema import VideoCreate,VideoUpdate


router=APIRouter()

@router.get("/")
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
@router.post("/")
def create_video_controller(video: VideoCreate, db: Session = Depends(get_db)):
    try:
        video = create_video(video, db)
        return video,status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#PUT /video/{video_id}
@router.put("/{video_id}")
def update_video_controller(video_id: str, video: VideoUpdate, db: Session = Depends(get_db)):
    try:
        video = update_video(video_id, video, db)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /video/{video_id}
@router.delete("/{video_id}")
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
    
    

@router.post("/{video_id}/like")
def like_video(video_id: str, enfant_id: str, db: Session = Depends(get_db)):
    try:
        liker_video(enfant_id, video_id, db)
        return {"message": "Video liked successfully"}, status.HTTP_200_OK
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{video_id}/consulter")
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
        raise HTTPException(status_code=500, detail="Caleb est un 10 ")
