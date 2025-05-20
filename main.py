from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="Digital Loan Application API")

# In-memory data stores
offers_db = {}
applications_db = {}

# Request Models
class LoanOfferRequest(BaseModel):
    customerId: str
    amount: float
    term: int

class LoanApplicationRequest(BaseModel):
    offerId: str
    signedDocs: str

# Response Models
class LoanOfferResponse(BaseModel):
    offerId: str
    interestRate: float
    approvedAmount: float
    term: int

class LoanApplicationStatus(BaseModel):
    applicationId: str
    status: str
    disbursed: bool

@app.post("/loan-offers/evaluate", response_model=LoanOfferResponse)
def evaluate_offer(req: LoanOfferRequest):
    offer_id = str(uuid4())
    interest_rate = 0.09 if req.amount < 5000 else 0.075
    offers_db[offer_id] = {
        "customerId": req.customerId,
        "amount": req.amount,
        "term": req.term,
        "interestRate": interest_rate
    }
    return LoanOfferResponse(
        offerId=offer_id,
        interestRate=interest_rate,
        approvedAmount=req.amount,
        term=req.term
    )

@app.post("/loan-applications", response_model=LoanApplicationStatus)
def create_application(req: LoanApplicationRequest):
    if req.offerId not in offers_db:
        raise HTTPException(status_code=404, detail="Offer not found")
    app_id = str(uuid4())
    applications_db[app_id] = {
        "offerId": req.offerId,
        "signedDocs": req.signedDocs,
        "status": "pending",
        "disbursed": False
    }
    return LoanApplicationStatus(applicationId=app_id, status="pending", disbursed=False)

@app.post("/loan-applications/{application_id}/approve", response_model=LoanApplicationStatus)
def approve_application(application_id: str):
    if application_id not in applications_db:
        raise HTTPException(status_code=404, detail="Application not found")
    applications_db[application_id]["status"] = "approved"
    applications_db[application_id]["disbursed"] = True
    return LoanApplicationStatus(
        applicationId=application_id,
        status="approved",
        disbursed=True
    )

@app.get("/loan-applications/{application_id}/status", response_model=LoanApplicationStatus)
def get_application_status(application_id: str):
    if application_id not in applications_db:
        raise HTTPException(status_code=404, detail="Application not found")
    app_data = applications_db[application_id]
    return LoanApplicationStatus(
        applicationId=application_id,
        status=app_data["status"],
        disbursed=app_data["disbursed"]
    )
