from pydantic import BaseModel,EmailStr

class AdminBase(BaseModel):
    id: str
    nom: str
    prenom: str
    contact: str
    email: str
class AdminCreate(AdminBase):
    motDePasse: str
   