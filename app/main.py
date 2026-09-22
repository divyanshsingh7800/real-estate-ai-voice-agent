from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.agent import RealEstateAgent
from app.database.database import get_all_leads

app = FastAPI(
    title = "Real Estate Voice Agent API",
    description = "AI-powered real estate lead qualification backend",
    version = "1.0.0"
)

agent = RealEstateAgent()

class MessageRequests(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "message": "Real Estate Voice Agent API is running",
        "status": "Success"
    }

@app.post("/chat")
def chat(requests: MessageRequests):
    result = agent.process_message(requests.message)

    return {
        "response": result.get("response"),
        "customer_data": result.get("customer_data"),
        "lead_id": result.get("lead_id")
    }

@app.get("/leads")
def get_leads():
    leads = get_all_leads()

    return {
        "count": len(leads),
        "leads": [dict(lead) for lead in leads]
    }