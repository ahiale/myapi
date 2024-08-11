from datetime import time
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

class Token(BaseModel):
    access_token:str
    token_type:str
    
class DataToken(BaseModel):
    id: Optional[str]=None
    
class AdminOutput (BaseModel):
    email:str
    id:int
    created_at:time
    class config:
        orm_mode=True

class LoginSchema(BaseModel):
    email: str
    password: str