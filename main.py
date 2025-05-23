from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CustomerInfo(BaseModel):
    name: str
    document_id: str

class CustomerOffer(BaseModel):
    customerInfo: CustomerInfo
    productType: str = "SavingsAccount"
    acceptanceStatus: str

class AccessEntitlement(BaseModel):
    customerId: str
    channels: List[str]
    devices: List[str]

class SavingsAccount(BaseModel):
    customerId: str
    currency: str
    initialDeposit: float
    terms: str

@app.post("/customer-offers")
def create_customer_offer(offer: CustomerOffer):
    return {"message": "Customer offer created", "offer": offer}

@app.post("/access-entitlements")
def create_access_entitlement(entitlement: AccessEntitlement):
    return {"message": "Access entitlement created", "entitlement": entitlement}

@app.post("/documents")
def upload_document(customerId: str, documentType: str, file: UploadFile = File(...)):
    return {"message": "Document uploaded", "filename": file.filename, "customerId": customerId, "documentType": documentType}

@app.post("/savings-accounts")
def create_savings_account(account: SavingsAccount):
    return {"message": "Savings account created", "account": account}

# Comando para correr: uvicorn main:app --reload
# Swagger UI disponible en: http://127.0.0.1:8000/docs
