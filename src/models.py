from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class BreastfeedingSession(Base):
    __tablename__ = "BreastfeedingSessions"

    SessionID = Column(Integer, primary_key=True, index=True)
    UserID = Column(String(255), index=True)
    Timestamp = Column(DateTime)
    Breast = Column(String(10))
