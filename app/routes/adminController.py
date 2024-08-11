from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from app.models.admin import Admin
from app.models.admin import Admin
# from schemas.adminSchema import AdminCreate, AdminUpdate 
from database import get_db
from app.crud.adminService import get_admin, get_all_admins, create_admin, login, update_admin, delete_admin
from app.crud.utils import generate_id
from app.schemas.adminSchema import AdminBase, AdminCreate, AdminUpdate, LoginSchema


router=APIRouter()

@router.get("/")
def readP(db: Session=Depends(get_db)):
    admins=get_all_admins(db)
    if not admins:
        raise HTTPException(status_code=404, detail="No admin found")
    return admins

# GET /admin/{admin_id}
@router.get("/getAdmin/{admin_id}")
def read_admin_controller(admin_id: str, db: Session = Depends(get_db)):
    try:
        admin = get_admin(admin_id, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /admin/
@router.post("/")
def create_admin_controller(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        admin = create_admin(admin, db)
        return admin,status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login")
def get_token(data: LoginSchema, db: Session = Depends(get_db)):
    token = login(data, db)
    return token


#PUT /admin/{admin_id}
@router.put("/{admin_id}")
def update_admin_controller(admin_id: str, admin: AdminUpdate, db: Session = Depends(get_db)):
    try:
        admin = update_admin(admin_id, admin, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /admin/{admin_id}
@router.delete("/{admin_id}")
def delete_admin_controller(admin_id: str, db: Session = Depends(get_db)):
    try:
        admin = get_admin(admin_id, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        response = delete_admin(admin_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete admin")
        return {"message": "Admin deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
