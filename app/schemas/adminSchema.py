from pydantic import BaseModel,EmailStr
from typing import List, Optional

class AdminBase(BaseModel):
    nom: str
    prenom: str
    contact: str
    email: EmailStr
    
class AdminCreate(AdminBase):
    motDePasse: str

class AdminUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    motDePasse: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    