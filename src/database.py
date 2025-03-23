import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
HOST_NAME=os.getenv("HOST_NAME")
HOST_PORT=os.getenv("HOST_PORT")
DB_NAME=os.getenv("DB_NAME")

# Create DB URL
DB_URL = f"mysql://{DB_USER}:{DB_PASS}@{HOST_NAME}:{HOST_PORT}/{DB_NAME}"

# Create SQLAlchemy engine and session
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
