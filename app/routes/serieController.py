from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.serie import Serie
# from schemas.serieSchema import SerieCreate, SerieUpdate 
from database import get_db
from app.crud.serieService import get_serie, get_all_series, create_serie, update_serie, delete_serie
from app.schemas.serieSchema import  SerieCreate, SerieUpdate


router=APIRouter()

@router.get("/")
def readP(db: Session=Depends(get_db)):
    series=get_all_series(db)
    if not series:
        raise HTTPException(status_code=404, detail="No serie found")
    return series

# GET /serie/{serie_id}
@router.get("/{serie_id}")
def read_serie_controller(serie_id: str, db: Session = Depends(get_db)):
    try:
        serie = get_serie(serie_id, db)
        if not serie:
            raise HTTPException(status_code=404, detail="Serie not found")
        return serie
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /serie/
@router.post("/")
def create_serie_controller(serie: SerieCreate, db: Session = Depends(get_db)):
    try:
        serie = create_serie(serie, db)
        return serie,status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



#PUT /serie/{serie_id}
@router.put("/{serie_id}")
def update_serie_controller(serie_id: str, serie: SerieUpdate, db: Session = Depends(get_db)):
    try:
        serie = update_serie(serie_id, serie, db)
        if not serie:
            raise HTTPException(status_code=404, detail="Serie not found")
        return serie,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /serie/{serie_id}
@router.delete("/{serie_id}")
def delete_serie_controller(serie_id: str, db: Session = Depends(get_db)):
    try:
        serie = get_serie(serie_id, db)
        if not serie:
            raise HTTPException(status_code=404, detail="Serie not found")
        response = delete_serie(serie_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete serie")
        return {"message": "Serie deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
