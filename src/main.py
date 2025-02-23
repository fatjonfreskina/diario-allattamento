from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import BreastfeedingSession
from schemas import BreastfeedingSessionCreate, BreastfeedingSessionResponse
from database import get_db, engine, Base
from fastapi.responses import JSONResponse
from pydantic import ValidationError

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/alexa/log_breastfeeding", response_model=BreastfeedingSessionResponse)
async def log_breastfeeding(data: BreastfeedingSessionCreate, db: Session = Depends(get_db)):
    # Simulating UserID from Alexa event (in production, extract it from the request)
    user_id = "example-user-id"
    
    # Insert the breastfeeding data into the database
    session = BreastfeedingSession(
        UserID=user_id,
        Timestamp=data.Timestamp,
        Breast=data.Breast
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return JSONResponse(content={
        "UserID": user_id,
        "Breast": session.Breast,
        "Timestamp": session.Timestamp.isoformat()
    })

@app.get("/alexa/last_feeding", response_model=BreastfeedingSessionResponse)
async def get_last_feeding(db: Session = Depends(get_db)):
    user_id = "example-user-id"
    
    session = db.query(BreastfeedingSession).filter(BreastfeedingSession.UserID == user_id).order_by(
        BreastfeedingSession.Timestamp.desc()).first()
    
    if session is None:
        raise HTTPException(status_code=404, detail="No breastfeeding sessions found")
    
    return BreastfeedingSessionResponse(
        UserID=session.UserID,
        Breast=session.Breast,
        Timestamp=session.Timestamp
    )
