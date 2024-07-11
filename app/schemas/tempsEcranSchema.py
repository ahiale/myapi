from pydantic import BaseModel
from datetime import time
from typing import Optional, Literal

class TempsEcranBase(BaseModel):
    joursA: Literal['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    heuresD: time
    heuresF: time
    enfant_id: str

    class Config:
        arbitrary_types_allowed = True

class TempsEcranCreate(TempsEcranBase):
    pass

class TempsEcranUpdate(BaseModel):
    heuresD: Optional[time] = None
    joursA: Optional[Literal['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']] = None
    heuresF: Optional[time] = None

    class Config:
        arbitrary_types_allowed = True
