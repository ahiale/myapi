from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from ..models.saison import Saison
# from schemas.saisonSchema import SaisonCreate, SaisonUpdate 
from database import get_db
from ..crud.saisonService import get_saison, get_all_saisons, create_saison, update_saison, delete_saison
from ..schemas.saisonSchema import SaisonBase, SaisonCreate, SaisonUpdate


router=APIRouter()

@router.get("/")
def readP(db: Session=Depends(get_db)):
    saisons=get_all_saisons(db)
    if not saisons:
        raise HTTPException(status_code=404, detail="No saison found")
    return saisons

# GET /saison/{saison_id}
@router.get("/{saison_id}")
def read_saison_controller(saison_id: str, db: Session = Depends(get_db)):
    try:
        saison = get_saison(saison_id, db)
        if not saison:
            raise HTTPException(status_code=404, detail="Saison not found")
        return saison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /saison/
@router.post("/")
def create_saison_controller(saison: SaisonCreate, db: Session = Depends(get_db)):
    try:
        saison = create_saison(saison, db)
        return saison,status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



#PUT /saison/{saison_id}
@router.put("/{saison_id}")
def update_saison_controller(saison_id: str, saison: SaisonUpdate, db: Session = Depends(get_db)):
    try:
        saison = update_saison(saison_id, saison, db)
        if not saison:
            raise HTTPException(status_code=404, detail="Saison not found")
        return saison,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /saison/{saison_id}
@router.delete("/{saison_id}")
def delete_saison_controller(saison_id: str, db: Session = Depends(get_db)):
    try:
        saison = get_saison(saison_id, db)
        if not saison:
            raise HTTPException(status_code=404, detail="Saison not found")
        response = delete_saison(saison_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete saison")
        return {"message": "Saison deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
