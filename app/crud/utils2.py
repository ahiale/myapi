
from passlib.hash import pbkdf2_sha256 # type: ignore
import uuid
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import app.schemas
import app.schemas.adminSchema 
from app.schemas.adminSchema import LoginSchema
from database import get_db
from  app import models
from app.models.admin import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "MTvlleCfHF1kBweAyyRRO3ufTajxeHvrqWyrcfmDx3r7HpvXbSG3JgRQUoCZLySz" 
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def generate_id2():
    return str(uuid.uuid4())[:30]

def get_hashed_password2(password: str) -> str:
    return pbkdf2_sha256.hash(password)



def verify_password2(password: str, hashed_pass: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_pass)

def create_access_token2(admin_id: str):

    to_encode= {"admin_id": admin_id}


    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"expire": expire.strftime("%Y-%m-d MH:M:AS")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access2(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        id: str= payload.get("admin_id")  
        if id is None:
             raise credentials_exception

        token_data = app.schemas.adminSchema(id=id)
        
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token_access2(token, credentials_exception)
    admin = db.query(Admin).filter(Admin.id == token.id).first()
    if not admin:
        raise credentials_exception

    return admin

