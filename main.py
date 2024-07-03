from fastapi import FastAPI,APIRouter
from app.routes import enfantController 
from fastapi import Depends


app = FastAPI()



router=APIRouter()
app.include_router(enfantController.router, prefix="/enfant", tags=["user"])

@app.get("/")
def read_root():
    return {"Hello": "World"}




