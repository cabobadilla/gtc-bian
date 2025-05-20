from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Digital Personal Loan API")

# === MODELS ===
class LoanApplicationRequest(BaseModel):
    customerId: str
    loanAmount: float
    term: int
    loanPurpose: Optional[str]

class CreditEvaluationRequest(BaseModel):
    customerId: str

class CreditEvaluationResponse(BaseModel):
    creditScore: int
    riskLevel: str
    approved: bool

class LoanOffer(BaseModel):
    offerId: str
    customerId: str
    approvedAmount: float
    interestRate: float
    term: int

class OfferAcceptance(BaseModel):
    offerId: str
    customerId: str

class LoanActivationRequest(BaseModel):
    customerId: str
    loanId: str

class CampaignOfferRequest(BaseModel):
    customerId: str
    offerId: str
    email: str

# === ROUTES ===
@app.post("/loan-application/initiate")
def initiate_loan_application(request: LoanApplicationRequest):
    return {"message": "Solicitud iniciada", "data": request.dict()}

@app.post("/credit-evaluation", response_model=CreditEvaluationResponse)
def evaluate_credit(request: CreditEvaluationRequest):
    credit_score = 720
    risk_level = "Low"
    approved = True if credit_score > 650 else False
    return CreditEvaluationResponse(
        creditScore=credit_score,
        riskLevel=risk_level,
        approved=approved
    )

@app.post("/loan-offer")
def present_loan_offer(request: LoanApplicationRequest):
    offer = LoanOffer(
        offerId="OFFER123",
        customerId=request.customerId,
        approvedAmount=request.loanAmount,
        interestRate=7.5,
        term=request.term
    )
    return offer

@app.post("/loan-offer/accept")
def accept_loan_offer(acceptance: OfferAcceptance):
    return {"message": "Oferta aceptada", "offerId": acceptance.offerId}

@app.post("/loan/activate")
def activate_loan(request: LoanActivationRequest):
    return {"message": "Préstamo activado", "loanId": request.loanId}

@app.post("/campaigns/send-offer")
def send_campaign_offer(request: CampaignOfferRequest):
    return {
        "message": "Oferta enviada por email",
        "email": request.email,
        "offerId": request.offerId
    }

@app.get("/campaigns/offer/{offer_id}")
def get_campaign_offer(offer_id: str):
    return {
        "offerId": offer_id,
        "approvedAmount": 10000.0,
        "interestRate": 7.5,
        "term": 24
    }
