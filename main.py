from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NegotiationRequest(BaseModel):
    carrier_offer: float
    original_rate: float
    negotiation_round: int
    last_offer: float

@app.post("/negotiate")
def negotiate(request: NegotiationRequest):
    max_offer = request.original_rate * 1.10
    
    if request.carrier_offer <= max_offer:
        return {"action": "ACCEPT", "agreed_rate": request.carrier_offer}
    elif request.negotiation_round >= 3:
        return {"action": "REJECT"}
    else:
        new_rate = (request.last_offer + max_offer) / 2
        return {
            "action": "COUNTER", 
            "new_rate": round(new_rate, 2),
            "negotiation_round": request.negotiation_round + 1
        }

@app.get("/health")
def health():
    return {"status": "healthy"}