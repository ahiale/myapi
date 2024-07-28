from pydantic import BaseModel
from typing import List, Optional

class EnfantBase(BaseModel):
    pseudo: str
    image_profil: Optional[str] = None
    age: int 
    code_pin: Optional[str] = None
    parent_id: str

class EnfantCreate(EnfantBase):
    pass

class EnfantUpdate(BaseModel):
    pseudo: Optional[str] = None
    image_profil: Optional[str] = None
    age: Optional[str] = None
    code_pin: Optional [str] 
    



