from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ParentBase(BaseModel):
    nom: str
    age: int
    pays: str
    contact: str = None
    email: EmailStr
    nbre_profil: str
    codeParental: str
    historique_video: Optional[str] = None
    admin_id:str

class ParentCreate(ParentBase):
    motDePasse: str
    

class ParentUpdate(BaseModel):
    nom: Optional[str] = None
    age: Optional[int] = None
    motDePasse: Optional[str] = None
    pays: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    codeParental: Optional[str] = None
    


