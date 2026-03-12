from chatbot.intents import INTENTS
from chatbot.nlp import detect_intent_nlp
from database import SessionLocal
from models import Booking
from models import Booking, Customer

# In-memory session storage
sessions = {}


def get_user_history(phone):
    db = SessionLocal()
    bookings = db.query(Booking).filter(Booking.phone == phone).all()
    db.close()
    return bookings


def generate_response(user_input: str, session_id: str, phone: str):

    user_input = user_input.lower()

    # Ensure session exists
    if session_id not in sessions:
        sessions[session_id] = {}

    state = sessions.get(session_id, {})

    # Get user history
    history = get_user_history(phone)

    if len(history) > 0:
        last_booking = history[-1]
        previous_bike = last_booking.bike_model
    else:
        previous_bike = None

    # -------------------------
    # GREETING
    # -------------------------

    if "hi" in user_input or "hello" in user_input:
        if previous_bike:
            return f"Welcome back! Your last booking was for a {previous_bike}. How can I help today?"
        else:
            return "Hello! How can I help with your bike today?"

    # -------------------------
    # BOOKING FLOW
    # -------------------------

    if state.get("flow") == "booking":

        if state.get("step") == 1:
            sessions[session_id]["name"] = user_input
            sessions[session_id]["step"] = 2
            return "Please enter your phone number."

        elif state.get("step") == 2:
            sessions[session_id]["phone"] = user_input
            sessions[session_id]["step"] = 3
            return "Which bike model do you have?"

        elif state.get("step") == 3:
            sessions[session_id]["bike_model"] = user_input

            db = SessionLocal()

            booking = Booking(
                name=sessions[session_id]["name"],
                phone=sessions[session_id]["phone"],
                bike_model=sessions[session_id]["bike_model"]
            )

            db.add(booking)
            db.commit()
            db.close()

            sessions.pop(session_id)

            return "🎉 Booking confirmed! Our workshop will contact you shortly."

    # -------------------------
    # BIKE NOT STARTING FLOW
    # -------------------------

    if state.get("flow") == "not_starting":

        if state.get("step") == 1:
            sessions[session_id]["step"] = 2
            return "Do you hear a clicking sound when trying to start?"

        elif state.get("step") == 2:
            sessions.pop(session_id)

            if "yes" in user_input:
                return "This is likely a battery issue. We recommend checking the battery voltage."
            else:
                return "It may be a spark plug or fuel supply issue. Please visit the workshop."

    # -------------------------
    # BRAKE ISSUE FLOW
    # -------------------------

    if state.get("flow") == "brake_issue":

        if state.get("step") == 1:
            sessions[session_id]["step"] = 2
            return "Does the noise happen when you apply brakes?"

        elif state.get("step") == 2:
            sessions.pop(session_id)

            if "yes" in user_input:
                return "This usually indicates worn brake pads. They may need replacement."
            else:
                return "It could be a rotor alignment issue. A mechanic should inspect it."
            
    # -------------------------
    # OVERHEATING FLOW
    # -------------------------

    if state.get("flow") == "overheating":

        if state.get("step") == 1:
            sessions[session_id]["step"] = 2
            return "Does the engine heat up quickly during short rides?"

        elif state.get("step") == 2:
            sessions.pop(session_id)

            if "yes" in user_input:
                return "This might indicate low engine oil or cooling issues."
            else:
                return "It may be normal heating, but we recommend checking coolant and oil."
    # -------------------------
    # MILEAGE FLOW
    # -------------------------

    if state.get("flow") == "poor_mileage":

        if state.get("step") == 1:
            sessions[session_id]["step"] = 2
            return "Have you recently serviced your bike?"

        elif state.get("step") == 2:
            sessions.pop(session_id)

            if "no" in user_input:
                return "Low mileage may be due to clogged air filters or dirty spark plugs."
            else:
                return "It may be due to riding conditions or tire pressure."
            


    # -------------------------
    # NLP INTENT DETECTION
    # -------------------------

    intent = detect_intent_nlp(user_input)

    if intent == "brake_issue":
        sessions[session_id] = {
            "flow": "brake_issue",
            "step": 1
        }
        return "Are your brakes making noise?"

    if intent == "overheating":
        sessions[session_id] = {
            "flow": "overheating",
            "step": 1
        }
        return "Is your engine overheating during rides?"

    if intent == "poor_mileage":
        sessions[session_id] = {
            "flow": "poor_mileage",
            "step": 1
        }
        return "Are you experiencing low mileage?"
    # -------------------------
    # SERVICE INTENT
    # -------------------------

    if intent == "service":
        return "Regular service costs around ₹1500–₹2000. Would you like to book an appointment?"

    # -------------------------
    # BOOKING CONFIRMATION
    # -------------------------

    if "yes" in user_input and state.get("flow") is None:
        sessions[session_id] = {
            "flow": "booking",
            "step": 1
        }
        return "Great! Please enter your name."
    db = SessionLocal()

    # Save booking
    booking = Booking(
        name=sessions[session_id]["name"],
        phone=sessions[session_id]["phone"],
        bike_model=sessions[session_id]["bike_model"]
    )

    db.add(booking)

    # Check if customer exists
    existing_customer = db.query(Customer).filter(
        Customer.phone == sessions[session_id]["phone"]
    ).first()

    if not existing_customer:
        customer = Customer(
            name=sessions[session_id]["name"],
            phone=sessions[session_id]["phone"]
        )
        db.add(customer)

    db.commit()
    db.close()
    # -------------------------
    # STARTING ISSUE FLOW
    # -------------------------

    if intent == "not_starting":
        sessions[session_id] = {
            "flow": "not_starting",
            "step": 1
        }
        return "Is it self-start or kick start?"

    # -------------------------
    # OTHER INTENTS
    # -------------------------

    if intent in INTENTS:
        return INTENTS[intent]["response"]

    # -------------------------
    # DEFAULT RESPONSE
    # -------------------------

    return "I'm not sure I understand. Could you describe your bike issue?"