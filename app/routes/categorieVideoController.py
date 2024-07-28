from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.admin import Admin
from app.models.admin import Admin
# from schemas.adminSchema import AdminCreate, AdminUpdate 
from database import get_db
from app.crud.categorieVideoService import create_categorie_video, retrive_categorie_videos, retrive_categorie_by_video_id, retrive_videos_by_categorie_id
from app.crud.utils import generate_id
from app.schemas.adminSchema import AdminBase, AdminCreate, AdminUpdate





router=APIRouter()

@router.get("/")
def readP(db: Session=Depends(get_db)):
    categorie_videos=retrive_categorie_videos(db)
    if not categorie_videos:
        raise HTTPException(status_code=404, detail="No match found")
    return categorie_videos

@router.get("/categories_by_video/{video_id}")
def get_categories_by_video_id(video_id: str, db: Session = Depends(get_db)):
    return retrive_categorie_by_video_id(video_id, db)

@router.get("/videos_by_categorie/{categorie_id}")
def get_videos_by_categorie_id(categorie_id: str, db: Session = Depends(get_db)):
    return retrive_videos_by_categorie_id(categorie_id, db)