from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.enfant import Enfant
from app.models.parent import Parent
# from schemas.parentSchema import ParentCreate, ParentUpdate 
from database import get_db
from app.crud.parentService import get_all_parents, get_parent, create_parent, update_parent, delete_parent
from app.crud.utils import generate_id
from app.schemas.parentSchema import ParentCreate,ParentUpdate
from app.crud.utils import create_access_token
from app.crud.parentService import login
from app.schemas.parentSchema import LoginSchema
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

router=APIRouter()

@router.get("/red_all_parents")
def readP(db: Session=Depends(get_db)):
    parents=get_all_parents(db)
    if not parents:
        raise HTTPException(status_code=404, detail="No parent found")
    return parents

# GET /parent/{parent_id}
@router.get("/get/{parent_id}")
def read_parent_controller(parent_id: str, db: Session = Depends(get_db)):
    try:
        parent = get_parent(parent_id, db)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        return parent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /parent/
@router.post("/create")
def create_parent_controller(parent: ParentCreate, db: Session = Depends(get_db)):
    try:
        parent = create_parent(parent, db)
        return parent,status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



#PUT /parent/{parent_id}
@router.put("/{parent_id}")
def update_parent_controller(parent_id: str, parent: ParentUpdate, db: Session = Depends(get_db)):
    try:
        parent = update_parent(parent_id, parent, db)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        return parent,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /parent/{parent_id}
@router.delete("/{parent_id}")
def delete_parent_controller(parent_id: str, db: Session = Depends(get_db)):
    try:
        parent = get_parent(parent_id, db)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        response = delete_parent(parent_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete parent")
        return {"message": "Parent deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login")
def get_token(data: LoginSchema, db: Session = Depends(get_db)):
    token = login(data, db)
    return token



