
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from ..crud.utils import create_access_token

router=APIRouter()

@router.get("/token")
def get_token(data: dict):
   token= create_access_token(data)
   return data