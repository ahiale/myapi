from pydantic import BaseModel
from typing import Optional

class SaisonBase(BaseModel):
   
    titre: str 
    nb_episodes: int 
    serie_id: str

class SaisonCreate(BaseModel):
    pass