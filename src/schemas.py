from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BreastfeedingSessionCreate(BaseModel):
    Breast: str
    Timestamp: Optional[datetime]

    class Config:
        orm_mode = True

class BreastfeedingSessionResponse(BaseModel):
    UserID: str
    Breast: str
    Timestamp: datetime

    class Config:
        orm_mode = True
