from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Credit Offer Automation API")

class CreditSimulationRequest(BaseModel):
    amount: float
    term: int
    customerId: str

class CreditSimulationResponse(BaseModel):
    monthlyPayment: float
    interestRate: float
    totalCost: float

class OfferAcceptanceRequest(BaseModel):
    offerId: str
    signature: str
    accountId: str

class LoanStatusResponse(BaseModel):
    status: str
    nextPaymentDue: str
    outstandingBalance: float

@app.post("/api/v1/credit/simulate", response_model=CreditSimulationResponse)
def simulate_credit(request: CreditSimulationRequest):
    # Dummy simulation logic
    interest_rate = 0.15
    monthly_payment = (request.amount * (1 + interest_rate)) / request.term
    total_cost = monthly_payment * request.term
    return CreditSimulationResponse(
        monthlyPayment=monthly_payment,
        interestRate=interest_rate,
        totalCost=total_cost
    )

@app.post("/api/v1/offer/accept", status_code=201)
def accept_offer(request: OfferAcceptanceRequest):
    # Dummy loan acceptance logic
    return {"message": "Offer accepted and loan created", "loanId": "LOAN123456"}

@app.get("/api/v1/loan/status", response_model=LoanStatusResponse)
def get_loan_status(loanId: str = Query(...)):
    # Dummy status retrieval logic
    return LoanStatusResponse(
        status="Active",
        nextPaymentDue="2025-06-15",
        outstandingBalance=9500.00
    )
