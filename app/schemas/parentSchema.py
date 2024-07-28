from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import time

class ParentBase(BaseModel):
    nom: str
    age: int
    pays: str
    contact: str = None
    email: EmailStr
    codeParental: str
    

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
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class DataToken(BaseModel):
    id: Optional[str]=None
    
class ParentOutput (BaseModel):
    email:str
    id:int
    created_at:time
    class config:
        orm_mode=True

class LoginSchema(BaseModel):
    email: str
    password: str