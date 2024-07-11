from fastapi import FastAPI
from app.routes import parentController, enfantController, adminController, tempsEcranController, videoController, saisonController, serieController, categorieController

app = FastAPI()

app.include_router(enfantController.router, prefix="/enfant", tags=["user"])
app.include_router(parentController.router, prefix="/parent", tags=["user"])
app.include_router(adminController.router, prefix="/admin", tags=["user"])
app.include_router(tempsEcranController.router, prefix="/tempsEcran", tags=["user"])
app.include_router(videoController.router, prefix="/video", tags=["user"])
app.include_router(saisonController.router, prefix="/saison", tags=["user"])
app.include_router(serieController.router, prefix="/serie", tags=["user"])
app.include_router(categorieController.router, prefix="/categorie", tags=["user"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

