from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from ..crud.utils2 import create_access_token2, generate_id2, get_hashed_password2, verify_password2
from ..models.admin import Admin
from ..models.admin import Admin
from ..schemas.adminSchema import AdminCreate, AdminUpdate, LoginSchema
from database import get_db
from ..crud.utils import  generate_id
import logging
import bcrypt

# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')

def retriveAdmin(admin_id: str, db:Session=Depends(get_db)):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def get_admin(admin_id: str, db:Session=Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet admin na pas ete trouve")
    return admin

def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    
    admin= db.query(Admin).filter(Admin.email == login_data.email).first()
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # var = verify_password(login_data.password, admin.motDePasse)
    if not verify_password2(login_data.password, admin.motDePasse):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token= create_access_token2(admin.id)
    return {"token": token, "id" : admin.id}

def create_admin(admin: AdminCreate, db:Session=Depends(get_db)):
    
    rand_id= generate_id2()
    while retriveAdmin(rand_id, db):
        rand_id=generate_id2()
        
    # Vérification d'unicité de l'email et du contact dans la base de données
    if db.query(Admin).filter(Admin.email == admin.email).first():
        raise HTTPException(status_code=422, detail="Cet email est déjà utilisé.")
    
    if admin.contact and db.query(Admin).filter(Admin.contact == admin.contact).first():
        raise HTTPException(status_code=422, detail="Ce contact est déjà utilisé.")
    
    
    hashed_password = get_hashed_password2(admin.motDePasse)
    
    db_admin = Admin(
        id=rand_id,
        nom= admin.nom,
        motDePasse=hashed_password,
        contact=admin.contact,
        email=admin.email,
    )
    
    try:
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin    
    except Exception as e:
        logging.error(f"Error fetching admins: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="International server error")


def update_admin(admin_id: str, admin_update: AdminUpdate, db:Session=Depends(get_db)):
    
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail=f"User with ID {admin_id} not found")
    
    admin.nom=admin_update.nom if admin_update.nom else admin.nom
    admin.prenom=admin_update.prenom if admin_update.prenom else admin.prenom
    admin.contact=admin_update.contact if admin_update.contact else admin.contact
    admin.email=admin_update.email if admin_update.email else admin.email
    admin.motDePasse=admin_update.motDePasse if admin_update.motDePasse else admin.motDePasse
    
    db.commit()
    db.refresh(admin)
    return admin

def delete_admin( admin_id: str, db:Session=Depends(get_db)):
    admin = get_admin(admin_id,db)
    if not admin:
        raise HTTPException(status_code=404, detail=f"User with ID {admin_id} not found")
    db.delete(admin)
    db.commit()
    return True


def get_all_admins(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all admins from the database")
        admins = db.query(Admin).all()
        logging.info(f"Fetched {len(admins)} admins")
        return admins
    except Exception as e:
        logging.error(f"Error fetching admins: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


