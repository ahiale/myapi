from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum as PyEnum

class TypeVideoEnum(PyEnum):
    FILM =1
    EPISODE =2

class VideoBase(BaseModel):
    titre: str
    description: str 
    duree: str 
    type_video: TypeVideoEnum 
    admin_id:str
    saison_id:str

    class Config:
        use_enum_values = True

class VideoCreate(VideoBase):
    
    url: HttpUrl
    admin_id:str
    saison_id:str
    
class VideoUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    duree: Optional[str] = None
    url: Optional[HttpUrl] = None
    type_video: Optional[TypeVideoEnum] = None
