# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from. import models
# SQLAlchemy database URL
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test1.db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:datapassword@localhost:5432/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for models
Base = declarative_base()
def init_db():
   
   models.Base.metadata.create_all(bind=engine) 

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
