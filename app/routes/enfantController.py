from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.enfant import Enfant
from app.models.parent import Parent
# from schemas.enfantSchema import EnfantCreate, EnfantUpdate 
from database import get_db
from app.crud.enfantService import get_enfant, get_all_enfants, create_enfant, update_enfant, delete_enfant, get_tempsEcran_by_enfant_id
from app.crud.utils import generate_id
from app.schemas.enfantSchema import EnfantCreate,EnfantUpdate


router=APIRouter()

@router.get("/read_all_enfants")
def readU(db: Session=Depends(get_db)):
    enfants=get_all_enfants(db)
    return enfants

# GET /enfant/{enfant_id}
@router.get("/{enfant_id}")
def read_enfant_controller(enfant_id: str, db: Session = Depends(get_db)):
    try:
        enfant = get_enfant(enfant_id, db)
        if not enfant:
            raise HTTPException(status_code=404, detail="Enfant not found")
        return enfant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /enfant/
@router.post("/createEnfant")
def create_enfant_controller(enfant: EnfantCreate, db: Session = Depends(get_db)):
    try:
        enfant = create_enfant(enfant, db)
        return enfant,status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#PUT /enfant/{enfant_id}
@router.put("/{enfant_id}")
def update_enfant_controller(enfant_id: str, enfant: EnfantUpdate, db: Session = Depends(get_db)):
    try:
        enfant = update_enfant(enfant_id, enfant, db)
        if not enfant:
            raise HTTPException(status_code=404, detail="Enfant not found")
        return enfant,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /enfant/{enfant_id}
@router.delete("/delete/{enfant_id}")
def delete_enfant_controller(enfant_id: str, db: Session = Depends(get_db)):
    try:
        enfant = get_enfant(enfant_id, db)
        if not enfant:
            raise HTTPException(status_code=404, detail="Enfant not found")
        response = delete_enfant(enfant_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete enfant")
        return {"message": "Enfant deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{enfant_id}/temps_ecran")
def get_tempsEcran(enfant_id: str, db: Session = Depends(get_db)):
    return get_tempsEcran_by_enfant_id(enfant_id, db)