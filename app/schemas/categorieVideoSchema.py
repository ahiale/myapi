from pydantic import BaseModel
from typing import List, Optional

class CategorieVideoBase(BaseModel):
    categorie_id: str
    video_id: str
    
    class config:
        orm_mode=True




class CategorieVideoCreate(CategorieVideoBase):
   pass

