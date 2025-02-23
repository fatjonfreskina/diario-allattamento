from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class BreastfeedingSession(Base):
    __tablename__ = "BreastfeedingSessions"

    SessionID = Column(Integer, primary_key=True, index=True)
    UserID = Column(String(255), index=True)
    Timestamp = Column(DateTime, default=datetime.utcnow)
    Breast = Column(String(10))

# Make sure to run this to create the table
# from database import engine
# Base.metadata.create_all(bind=engine)
