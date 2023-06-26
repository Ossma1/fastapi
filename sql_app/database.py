from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#pourconnecter avec fichier sqlite qui existe dans meme repertoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#connectarg just pour sqlite pour plusieur thread
    
engine = create_engine( 
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#copier dyal base dedonner
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#class pere pour creer des class modele
Base = declarative_base()
#session.query(User).all() traitement <= sessionlocal pour ouvrir session au debut