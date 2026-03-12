from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from chatbot.engine import generate_response
from database import engine, Base
import models
from database import SessionLocal
from models import Booking, Customer
from datetime import datetime
from fastapi import FastAPI
from database import Base, engine
import models


app = FastAPI()

# create tables automatically
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str
    session_id: str
    phone: str
from fastapi.staticfiles import StaticFiles

app.mount("/widget", StaticFiles(directory="frontend"), name="widget")

from fastapi.staticfiles import StaticFiles

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return {"message": "RideCare Smart Chatbot with Memory 🚀"}

@app.post("/chat")
def chat(message: Message):
    reply = generate_response(message.text, message.session_id, message.phone)
    return {"reply": reply}


@app.get("/stats")
def get_stats():

    db = SessionLocal()

    total_bookings = db.query(Booking).count()
    total_customers = db.query(Customer).count()

    db.close()

    return {
        "total_bookings": total_bookings,
        "total_customers": total_customers
    }

@app.get("/bookings")
def get_bookings():

    db = SessionLocal()

    bookings = db.query(Booking).all()

    result = []

    for b in bookings:
        result.append({
            "name": b.name,
            "phone": b.phone,
            "bike_model": b.bike_model
        })

    db.close()

    return result

@app.get("/customers")
def get_customers():

    db = SessionLocal()

    customers = db.query(Customer).all()

    result = []

    for c in customers:
        result.append({
            "name": c.name,
            "phone": c.phone
        })

    db.close()

    return result