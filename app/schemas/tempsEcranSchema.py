from pydantic import BaseModel
from datetime import time
from typing import List, Optional, Literal

class TempsEcranBase(BaseModel):
    joursA: Optional[List[str]]
    heuresD: Optional[time]
    heuresF: Optional[time]
    enfant_id: str

    class Config:
        arbitrary_types_allowed = True

class TempsEcranCreate(TempsEcranBase):
    pass

class TempsEcranUpdate(BaseModel):
    heuresD: Optional[time] = None
    joursA: Optional[List[str]] = None
    heuresF: Optional[time] = None

    class Config:
        arbitrary_types_allowed = True
