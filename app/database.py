import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")  

# Crea el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Crea una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define la clase base para los modelos
Base = declarative_base()

def init_db():
    """
    Crea todas las tablas definidas en los modelos que hereden de Base.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependencia que crea y cierra una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
