from pydantic import BaseModel
from typing import Optional

class SaisonBase(BaseModel):
   
    titre: str 
    nb_episodes: int 
    serie_id: str

class SaisonCreate(SaisonBase):
    pass

class SaisonUpdate(BaseModel):
    titre: Optional[str] = None
    nb_episodes: Optional[int] = None