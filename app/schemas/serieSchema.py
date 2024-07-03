from pydantic import BaseModel
from typing import Optional

class SerieBase(BaseModel):
    titre: str 
    description: str
    nb_saisons: int

class SerieCreate(SerieBase):
    pass

class SerieUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    nb_saisons: Optional[int] = None
