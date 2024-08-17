from datetime import datetime
import json
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends,APIRouter
from ..models.tempsEcran import TempsEcran
from ..models.enfant import Enfant
# from schemas.tempsEcranSchema import TempsEcranCreate, TempsEcranUpdate 
from database import get_db
from ..crud.tempsEcranService import get_tempsEcran, get_all_tempsEcrans, create_tempsEcran, update_tempsEcran, delete_tempsEcran, get_enfant_id_by_temps_ecran_id
from ..crud.utils import generate_id
from ..schemas.tempsEcranSchema import TempsEcranCreate,TempsEcranUpdate


router=APIRouter()

@router.get("/")
def readU(db: Session=Depends(get_db)):
    tempsEcrans=get_all_tempsEcrans(db)
    if not tempsEcrans:
        raise HTTPException(status_code=404, detail="No tempsEcran found")
    return tempsEcrans

# GET /tempsEcran/{tempsEcran_id}
@router.get("/{tempsEcran_id}")
def read_tempsEcran_controller(tempsEcran_id: str, db: Session = Depends(get_db)):
    try:
        tempsEcran = get_tempsEcran(tempsEcran_id, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        return tempsEcran
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# POST /tempsEcran/
@router.post("/CreateTempsEcran")
def create_tempsEcran_controller(tempsEcran: TempsEcranCreate, db: Session = Depends(get_db)):
    try:
        tempsEcran = create_tempsEcran(tempsEcran, db)
        return tempsEcran,status.HTTP_201_CREATED
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#PUT /tempsEcran/{tempsEcran_id}
@router.put("/{tempsEcran_id}")
def update_tempsEcran_controller(tempsEcran_id: str, tempsEcran: TempsEcranUpdate, db: Session = Depends(get_db)):
    try:
        tempsEcran = update_tempsEcran(tempsEcran_id, tempsEcran, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        return tempsEcran,status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#DELETE /tempsEcran/{tempsEcran_id}
@router.delete("/{tempsEcran_id}")
def delete_tempsEcran_controller(tempsEcran_id: str, db: Session = Depends(get_db)):
    try:
        tempsEcran = get_tempsEcran(tempsEcran_id, db)
        if not tempsEcran:
            raise HTTPException(status_code=404, detail="TempsEcran not found")
        response = delete_tempsEcran(tempsEcran_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete tempsEcran")
        return {"message": "TempsEcran deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tempsEcran_id}/enfant_id")
def get_enfant_id(tempsEcran_id: str, db: Session = Depends(get_db)):
    return get_enfant_id_by_temps_ecran_id(tempsEcran_id, db)


@router.get("/check-screen-time/{enfant_id}")
def check_screen_time(enfant_id: str, db: Session = Depends(get_db)):
    
    french_to_weekday = {
    "lundi": 0,
    "mardi": 1,
    "mercredi": 2,
    "jeudi": 3,
    "vendredi": 4,
    "samedi": 5,
    "dimanche": 6
}
   
    # Récupérer le temps d'écran pour l'enfant
    temps_ecran = db.query(TempsEcran).filter(TempsEcran.enfant_id == enfant_id).first()
    
    if not temps_ecran:
        raise HTTPException(status_code=404, detail="Temps d'écran non trouvé pour cet enfant")
    
    jour_list=temps_ecran.joursA.strip('{}').split(',')
    weekday_numbers = {french_to_weekday[day.lower()] for day in jour_list}
    # Heure actuelle
    heure_actuelle = datetime.now().time()
    today = datetime.today()
    
    if today.weekday() not in weekday_numbers:
        return {"status": "daysexpired", "message": "Vous n'etes pas autorises a vous connecter aujourdhui"}
        
    if heure_actuelle < temps_ecran.heuresD or heure_actuelle>temps_ecran.heuresF:
        
        return {"status": "expired", "message": "Le temps d'écran est écoulé"}
    
    return {"status": "ok", "message": "Le temps d'écran est toujours en cours"}