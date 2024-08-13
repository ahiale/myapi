from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from ..models.parent import Parent
from ..schemas.parentSchema import ParentCreate, ParentUpdate
from database import get_db
from ..crud.utils import generate_id
import logging
import bcrypt
from ..schemas.parentSchema import LoginSchema
from ..crud.utils import verify_password, create_access_token, get_hashed_password


# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')


def retriveParent(parent_id: str, db:Session=Depends(get_db)):
    return db.query(Parent).filter(Parent.id == parent_id).first()
    
def get_parent(parent_id: str, db:Session=Depends(get_db)):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cet parent n'a pas ete trouve")
    return parent

def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    
    parent= db.query(Parent).filter(Parent.email == login_data.email).first()
    
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # var = verify_password(login_data.password, parent.motDePasse)
    if not verify_password(login_data.password, parent.motDePasse):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token= create_access_token(parent.id)
    return {"token": token, "id" : parent.id}

def create_parent(parent: ParentCreate, db:Session=Depends(get_db)):
    
    rand_id= generate_id()
    while retriveParent(rand_id, db):
        rand_id=generate_id()
        
    # Vérification d'unicité de l'email et du contact dans la base de données
    if db.query(Parent).filter(Parent.email == parent.email).first():
        raise HTTPException(status_code=422, detail="Cet email est déjà utilisé.")
    
    if parent.contact and db.query(Parent).filter(Parent.contact == parent.contact).first():
        raise HTTPException(status_code=422, detail="Ce contact est déjà utilisé.")
    
    
    hashed_password = get_hashed_password(parent.motDePasse)
    
    db_parent = Parent(
        id=rand_id,
        nom= parent.nom,
        motDePasse=hashed_password,
        pays=parent.pays,
        email=parent.email,
        codeParental=parent.codeParental,
        age=parent.age,
        
    )
    
    try:
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
        return db_parent    
    except Exception as e:
        logging.error(f"Error fetching parents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="International server error")
    

def update_parent(parent_id: str, parent_update: ParentUpdate, db:Session=Depends(get_db)):
    
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    
    if not parent:
        raise HTTPException(status_code=404, detail=f"User with ID {parent_id} not found")
    
    
    parent.nom=parent_update.nom if parent_update.nom else parent.nom
    parent.age=parent_update.age if parent_update.age else parent.age
    parent.motDePasse=parent_update.motDePasse if parent_update.motDePasse else parent.motDePasse
    parent.codeParental=parent_update.codeParental if parent_update.codeParental else parent.codeParental
    parent.email=parent_update.email if parent_update.email else parent.email
    parent.contact=parent_update.contact if parent_update.contact else parent.contact
    parent.pays=parent_update.pays if parent_update.pays else parent.pays
    
    db.commit()
    db.refresh(parent)
    return parent

def delete_parent( Parent_id: str, db:Session=Depends(get_db)):
    parent = get_parent(Parent_id,db)
    if not parent:
        raise HTTPException(status_code=404, detail=f"User with ID {Parent_id} not found")
    db.delete(parent)
    db.commit()
    return True
    

# def get_all_parents(db:Session = Depends(get_db)):
#     return db.query(parent).all()
     
#     # return "parents"
    
    
    

def get_all_parents(db: Session = Depends(get_db)):
    try:
        logging.info("Fetching all parents from the database")
        parents = db.query(Parent).all()
        print(parents)
        logging.info(f"Fetched {len(parents)} parents")
        return parents
    except Exception as e:
        logging.error(f"Error fetching parents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    



