import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
DB_HOST_NAME=os.getenv("DB_HOST_NAME")
DB_PORT=os.getenv("DB_PORT")

# Create DB URL
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_PORT}/{DB_NAME}"

# Access environment variables
DB_URL=os.getenv("DB_URL")

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
