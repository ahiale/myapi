from pydantic import BaseModel,EmailStr
from typing import List, Optional

class CategorieBase(BaseModel):
    titre: str
    
    class config:
        orm_mode=True

class CategorieCreate(CategorieBase):
    pass

class CategorieUpdate(BaseModel):
    titre: Optional[str] = None