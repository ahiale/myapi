from pydantic import BaseModel
from typing import List, Optional

class EnfantBase(BaseModel):
    pseudo: str
    image_profil: Optional[str] = None
    age: int
    allocation:str
    joursA: List[str] 
    heuresA: List[str] 
    code_pin: List[str] 
    historique_video: List[str] 
    code_pin: Optional[str] = None
    parent_id: str

class EnfantCreate(EnfantBase):
    pass

class EnfantUpdate(BaseModel):
    pseudo: Optional[str] = None
    image_profil: Optional[int] = None
    age: Optional[int] = None
    allocation: Optional[str] = None
    joursA: Optional [List[str]] = None
    heuresA: Optional [List[str]] =None
    code_pin: Optional [str] 
    historique_video: Optional [List[str]]=None
    


