from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.tempsEcran import TempsEcran
from app.models.enfant import Enfant
# from schemas.tempsEcranSchema import TempsEcranCreate, TempsEcranUpdate 
from database import get_db
from app.crud.tempsEcranService import get_tempsEcran, get_all_tempsEcrans, create_tempsEcran, update_tempsEcran, delete_tempsEcran
from app.crud.utils import generate_id
from app.schemas.tempsEcranSchema import TempsEcranCreate,TempsEcranUpdate


router=APIRouter()

@router.get("/")
def readU(db: Session=Depends(get_db)):
    tempsEcrans=get_all_tempsEcrans(db)
    if not tempsEcrans:
        raise HTTPException(status_code=404, detail="No tempsEcran found")
    return tempsEcrans

# GET /tempsEcran/{tempsEcran_id}
@router.get("/{tempsEcran_id}")
def read_tempsEcran_controller(tempsEcran_id: str, db: Session = Depends(get_db)):
    try:
        tempsEcran = get_tempsEcran(tempsEcran_id, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        return tempsEcran
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /tempsEcran/
@router.post("/")
def create_tempsEcran_controller(tempsEcran: TempsEcranCreate, db: Session = Depends(get_db)):
    try:
        tempsEcran = create_tempsEcran(tempsEcran, db)
        return tempsEcran,status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#PUT /tempsEcran/{tempsEcran_id}
@router.put("/{tempsEcran_id}")
def update_tempsEcran_controller(tempsEcran_id: str, tempsEcran: TempsEcranUpdate, db: Session = Depends(get_db)):
    try:
        tempsEcran = update_tempsEcran(tempsEcran_id, tempsEcran, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        return tempsEcran,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /tempsEcran/{tempsEcran_id}
@router.delete("/{tempsEcran_id}")
def delete_tempsEcran_controller(tempsEcran_id: str, db: Session = Depends(get_db)):
    try:
        tempsEcran = get_tempsEcran(tempsEcran_id, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        response = delete_tempsEcran(tempsEcran_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete tempsEcran")
        return {"message": "TempsEcran deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    