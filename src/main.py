from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models import BreastfeedingSession
from database import get_db, engine, Base
from fastapi.responses import JSONResponse
import pytz
from datetime import datetime
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
import json

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/alexa/breastfeeding")

# Setup logging
logging.basicConfig(level=logging.INFO)

sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Benvenuta nel tuo diario di allattamento. Puoi chiedermi di registrare una sessione di allattamento o di recuperare l'ultima sessione registrata. Cosa vuoi fare?"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class RetrieveBreastfeedingIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RetrieveBreastfeedingIntent")(handler_input)

    def handle(self, handler_input):
        # Access the database
        db = next(get_db())
        user_id = handler_input.request_envelope.session.user.user_id

        # Retrieve the last breastfeeding session
        sessions = db.query(BreastfeedingSession).filter_by(UserID=user_id).order_by(BreastfeedingSession.Timestamp.desc()).limit(1).all()
        
        if len(sessions) == 0:
            speech_text = "Nessuna sessione di allattamento registrata."
        else:
            session = sessions[0]
            speech_text = f"L'ultimo allattamento è stato a {session.Breast}, alle {session.Timestamp.strftime('%H:%M')}."
        
        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

class LogBreastfeedingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LogBreastfeedingIntent")(handler_input)

    def handle(self, handler_input):
        # Extract slots and process the request
        slots = handler_input.request_envelope.request.intent.slots
        timestamp = handler_input.request_envelope.request.timestamp
        breast = slots["Breast"].value

        # Log the data
        logging.info(f"Timestamp: {timestamp}, Breast: {breast}")

        # Convert UTC timestamp to local timezone
        local_tz = pytz.timezone("Europe/Rome")  # Replace with your local timezone
        local_time = timestamp.astimezone(local_tz)
        
        logging.info(f"Local time: {local_time}")

        # Access the database
        db = next(get_db())
        user_id = handler_input.request_envelope.session.user.user_id

        # Create a new breastfeeding session
        new_session = BreastfeedingSession(
            UserID=user_id,
            Timestamp=local_time,  # Use the local time
            Breast=breast
        )

        # Add the session to the database
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        # Return a valid Alexa response
        speech_text = "Fatto."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RetrieveBreastfeedingIntent())
sb.add_request_handler(LogBreastfeedingIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())


lambda_handler = sb.lambda_handler()

@app.post("/")
async def alexa_webhook(request: Request):
    body = await request.body()
    response = lambda_handler(json.loads(body), None)
    return JSONResponse(content=response)