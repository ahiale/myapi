from importlib.metadata import files
from fastapi import File, UploadFile
from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum as PyEnum

from app.models.enumsVideos import Type_Source_Enum

class TypeVideoEnum(PyEnum):
    FILM =1
    EPISODE =2
    

class TypeSourceEnum(PyEnum):
    YOUTUBE =1
    DAILYMOTION=2
    ANIMESAMA=3
    UPLOAD=4

class VideoBase(BaseModel):
    # couverture:UploadFile = File(...)
    titre: str
    description: str 
    duree: str 
    type_video: TypeVideoEnum 
    url: HttpUrl
    type_source:TypeSourceEnum
    admin_id:str
    saison_id:str

    class Config:
        use_enum_values = True
        orm_mode=True
        

class VideoCreate(VideoBase):
    categorie_id:str
    admin_id:Optional[str] = None
    saison_id:Optional[str] = None

    
class VideoUpdate(BaseModel):
    # couverture: Optional[UploadFile] = File(...)
    titre: Optional[str] = None
    description: Optional[str] = None
    duree: Optional[str] = None
    type_video: Optional[TypeVideoEnum] = None
    url: Optional[HttpUrl] = None
    type_source: Optional[TypeSourceEnum] = None

class SearchCriteria(BaseModel):
    query: str =None # La chaîne de recherche que l'enfant entre
    # categorie: str = None  # Optionnel: catégorie spécifique de vidéo
