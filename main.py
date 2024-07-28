from fastapi import FastAPI
from app.routes import parentController, enfantController, adminController, tempsEcranController, videoController, saisonController, serieController, categorieController, categorieVideoController 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost:3000",  # L'origine de votre application frontend
    "http://localhost:8000",  # L'origine de votre API FastAPI (si nécessaire)
    # Ajoutez d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permettre ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Permettre toutes les méthodes HTTP
    allow_headers=["*"],  # Permettre tous les en-têtes
)

app.include_router(enfantController.router, prefix="/enfant", tags=["enfant"])
app.include_router(parentController.router, prefix="/parent", tags=["parent"])
app.include_router(adminController.router, prefix="/admin", tags=["admin"])
app.include_router(tempsEcranController.router, prefix="/tempsEcran", tags=["tempsEcran"])
app.include_router(videoController.router, prefix="/video", tags=["video"])
app.include_router(saisonController.router, prefix="/saison", tags=["saison"])
app.include_router(serieController.router, prefix="/serie", tags=["serie"])
app.include_router(categorieController.router, prefix="/categorie", tags=["categorie"])
app.include_router(categorieVideoController.router, prefix="/categorie_video", tags=["categorie_video"])
# app.include_router(auth.router, prefix="/categorie", tags=["categorie"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


