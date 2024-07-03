from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.enfant import Enfant
from app.models.parent import Parent
# from schemas.enfantSchema import EnfantCreate, EnfantUpdate 
from database import get_db
from app.crud.enfantService import get_enfant, get_all_enfants, create_enfant, update_enfant, delete_enfant
from app.crud.utils import generate_id

router=APIRouter()

@router.get("/read_enfant")
def readU(db: Session=Depends(get_db)):
    enfants=get_all_enfants(db)
    if not enfants:
        raise HTTPException(status_code=404, detail="No users found")
    return enfants