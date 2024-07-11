from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.categorie import Categorie
# from schemas.categorieSchema import CategorieCreate, CategorieUpdate 
from database import get_db
from app.crud.categorieService import get_categorie, get_all_categories, create_categorie, update_categorie, delete_categorie
from app.schemas.categorieSchema import CategorieBase, CategorieCreate, CategorieUpdate


router=APIRouter()

@router.get("/")
def readP(db: Session=Depends(get_db)):
    categories=get_all_categories(db)
    if not categories:
        raise HTTPException(status_code=404, detail="No categorie found")
    return categories

# GET /categorie/{categorie_id}
@router.get("/{categorie_id}")
def read_categorie_controller(categorie_id: str, db: Session = Depends(get_db)):
    try:
        categorie = get_categorie(categorie_id, db)
        if not categorie:
            raise HTTPException(status_code=404, detail="Categorie not found")
        return categorie
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /categorie/
@router.post("/")
def create_categorie_controller(categorie: CategorieCreate, db: Session = Depends(get_db)):
    try:
        categorie = create_categorie(categorie, db)
        return categorie,status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



#PUT /categorie/{categorie_id}
@router.put("/{categorie_id}")
def update_categorie_controller(categorie_id: str, categorie: CategorieUpdate, db: Session = Depends(get_db)):
    try:
        categorie = update_categorie(categorie_id, categorie, db)
        if not categorie:
            raise HTTPException(status_code=404, detail="Categorie not found")
        return categorie,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /categorie/{categorie_id}
@router.delete("/{categorie_id}")
def delete_categorie_controller(categorie_id: str, db: Session = Depends(get_db)):
    try:
        categorie = get_categorie(categorie_id, db)
        if not categorie:
            raise HTTPException(status_code=404, detail="Categorie not found")
        response = delete_categorie(categorie_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete categorie")
        return {"message": "Categorie deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
