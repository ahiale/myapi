from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de connexion à la base de données
DB_URL = "postgresql://nunyatoonbd_user:n70tHPS714TL8oMBFvuvVzzfTQ97GPag@dpg-cqvinetds78s739kbvpg-a.oregon-postgres.render.com/nunyatoonbd"

# Création du moteur SQLAlchemy
engine = create_engine(DB_URL)

# Configuration de la session
SessionLocal = sessionmaker(bind=engine)

# Création de la base déclarative
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Création de l'objet MetaData directement
metadata = MetaData()
