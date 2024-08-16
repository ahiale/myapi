from datetime import datetime, timedelta, timezone
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from ..models.parent import Parent
# from schemas.parentSchema import ParentCreate, ParentUpdate 
from database import SessionLocal, get_db
from ..crud.ParentService import get_all_parents, get_parent, create_parent, update_parent, delete_parent
from ..crud.utils import generate_id
from ..schemas.parentSchema import ParentCreate,ParentUpdate
from ..crud.utils import create_access_token
from ..crud.ParentService import login
from ..schemas.parentSchema import LoginSchema


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
@router.put("/updateParent/{parent_id}")
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


@router.get("/stats/registrations-per-day")
def get_registrations_per_day():
    try:
        db: Session = SessionLocal()
        
        today = datetime.now()
        one_month_ago = today - timedelta(days=30)

        registrations = db.query(Parent).filter(Parent.date_inscription >= one_month_ago).all()

        # Créer un dictionnaire pour compter les inscriptions par jour
        registration_counts = {}
        for parent in registrations:
            day = parent.date_inscription.strftime("%Y-%m-%d")
            if day in registration_counts:
                registration_counts[day] += 1
            else:
                registration_counts[day] = 1

        # Formater les données pour la réponse
        response = {"registrations_per_day": []}
        for day, count in registration_counts.items():
            response["registrations_per_day"].append({"date": day, "count": count})
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{parent_id}/contact")
def get_contact(parent_id: str, db: Session = Depends(get_db)):
    """Retourne le contact d'un parent grâce à son ID ou null si non trouvé."""
    query = select(Parent).filter_by(id=parent_id)
    parent = db.execute(query).scalars().first()
    if parent:
        return {"contact": parent.contact}
    else:
        return {"contact": None}
    
