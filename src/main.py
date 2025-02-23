from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models import BreastfeedingSession
from database import get_db, engine, Base
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/alexa/breastfeeding")

@app.post("/")
async def alexa_webhook(request: Request):
    body = await request.json()
    logging.info(f"Request Body: {body}")
    
    # Process the request, log data, etc.
    
    # Return a valid Alexa response
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Breastfeeding log saved!",
                "playBehavior": "REPLACE_ENQUEUED"
            },
            "card": {
                "type": "Standard",
                "title": "Breastfeeding Log",
                "text": "Your breastfeeding session has been logged.",
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Would you like to add another log?",
                    "playBehavior": "REPLACE_ENQUEUED"
                }
            },
            "directives": [],
            "shouldEndSession": True
        }
    }

@app.post("/alexa/log_breastfeeding")
async def log_breastfeeding(request: Request, db: Session = Depends(get_db)):
    try:
        # Get JSON data from the request
        data = await request.json()

        # Simulate extracting UserID from Alexa event (in production, extract it from Alexa context)
        user_id = "example-user-id"
        
        # Extract and validate required fields from the JSON
        timestamp = data.get("Timestamp")
        breast = data.get("Breast")

        if not timestamp or not breast:
            raise HTTPException(status_code=400, detail="Missing required fields 'Timestamp' or 'Breast'")

        # Convert timestamp to a datetime object
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid timestamp format")
        
        # Insert the breastfeeding data into the database
        session = BreastfeedingSession(
            UserID=user_id,
            Timestamp=timestamp,
            Breast=breast
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return JSONResponse(content={
            "UserID": user_id,
            "Breast": session.Breast,
            "Timestamp": session.Timestamp.isoformat()
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/alexa/last_feeding")
async def get_last_feeding(db: Session = Depends(get_db)):
    user_id = "example-user-id"
    
    # Query the last breastfeeding session for the user
    session = db.query(BreastfeedingSession).filter(BreastfeedingSession.UserID == user_id).order_by(
        BreastfeedingSession.Timestamp.desc()).first()
    
    if session is None:
        raise HTTPException(status_code=404, detail="No breastfeeding sessions found")

    return JSONResponse(content={
        "UserID": session.UserID,
        "Breast": session.Breast,
        "Timestamp": session.Timestamp.isoformat()
    })
