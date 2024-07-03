from pydantic import BaseModel,EmailStr
from typing import List, Optional

class CategorieBase(BaseModel):
    id: str
    titre: str

class CategorieCreate(BaseModel):
    titre: str

class CategorieUpdate(BaseModel):
    titre: Optional[str] = None