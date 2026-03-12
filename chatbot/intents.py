INTENTS = {
    "not_starting": {
        "keywords": ["not starting", "won't start", "self not working", "kick not working"],
        "response": "It could be a battery, spark plug, or fuel supply issue. Do you hear a clicking sound?"
    },
    "service": {
        "keywords": ["service", "regular service", "oil change"],
        "response": "Regular service costs between ₹1500 - ₹2000. Would you like to book an appointment?"
    },
    "brake_issue": {
        "keywords": ["brake", "brakes", "brake problem"],
        "response": "Brake issues are often due to worn brake pads or low brake oil. Is the brake making noise?"
    },
    "pricing": {
        "keywords": ["price", "cost", "how much"],
        "response": "Please tell me your bike model and service type so I can estimate cost."
    }
}
INTENTS = {

    "not_starting": {
        "keywords": [
            "not starting",
            "bike won't start",
            "engine not starting",
            "motorcycle not starting"
        ],
        "response": "Let's diagnose the starting problem."
    },

    "brake_issue": {
        "keywords": [
            "brake noise",
            "brake problem",
            "brakes making sound",
            "squeaky brakes"
        ],
        "response": "Let's check your brake issue."
    },

    "overheating": {
        "keywords": [
            "engine overheating",
            "bike getting hot",
            "engine too hot"
        ],
        "response": "Let's check why your engine is overheating."
    },

    "poor_mileage": {
        "keywords": [
            "poor mileage",
            "low mileage",
            "fuel consumption high"
        ],
        "response": "Let's check why your mileage is low."
    },

    "service": {
        "keywords": [
            "service",
            "bike service",
            "need service"
        ],
        "response": "Regular service costs around ₹1500–₹2000."
    }

}