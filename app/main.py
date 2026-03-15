from typing import Optional
from decimal import Decimal
from datetime import datetime
from uuid import uuid4
from pathlib import Path

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator, model_validator


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="IPN P2P Payment API")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

USED_CLIENT_REFERENCES = set()


class PaymentRequest(BaseModel):
    clientReference: str = Field(..., min_length=1, max_length=50)
    senderAccountNumber: str
    receiverAccountNumber: str
    amount: Decimal
    currency: str
    reference: str = Field(..., min_length=1, max_length=50)

    @field_validator("senderAccountNumber", "receiverAccountNumber")
    @classmethod
    def validate_account_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Account number must contain digits only.")
        if len(value) < 10:
            raise ValueError("Account number must be at least 10 digits.")
        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        if value != "NAD":
            raise ValueError("Currency must be NAD.")
        return value

    @field_validator("reference")
    @classmethod
    def validate_reference(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Reference must not be empty.")
        if len(value) > 50:
            raise ValueError("Reference must not exceed 50 characters.")
        return value

    @model_validator(mode="after")
    def validate_accounts_are_different(self):
        if self.senderAccountNumber == self.receiverAccountNumber:
            raise ValueError("Sender and receiver account numbers must be different.")
        return self


class PaymentResponse(BaseModel):
    status: str
    errorCode: Optional[str] = None
    transactionId: Optional[str] = None
    message: str


def generate_transaction_id() -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = uuid4().hex[:8].upper()
    return f"TXN-{date_part}-{random_part}"


def build_error_response(error_code: str, message: str, http_status: int):
    raise HTTPException(
        status_code=http_status,
        detail={
            "status": "FAILED",
            "errorCode": error_code,
            "transactionId": None,
            "message": message
        }
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# P2P payment endpoint used for the integration challenge.
# Simulates payment processing according to the provided mock API specification.
@app.post("/api/p2p-payment", response_model=PaymentResponse)
def create_p2p_payment(payload: PaymentRequest):

     # Ensure clientReference is unique per transaction
    if payload.clientReference in USED_CLIENT_REFERENCES:
        build_error_response(
            error_code="ERR001",
            message="Duplicate client reference.",
            http_status=status.HTTP_409_CONFLICT
        )

    # Simulate insufficient funds scenario for testing purposes
    if payload.amount > Decimal("5000.00"):
        build_error_response(
            error_code="ERR005",
            message="Insufficient funds.",
            http_status=status.HTTP_402_PAYMENT_REQUIRED
        )

     # Simulate internal processing failure when reference contains "error"
    if "error" in payload.reference.lower():
        build_error_response(
            error_code="ERR006",
            message="Internal processing error.",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

     # Mark the client reference as used only after validation and processing checks pass
    USED_CLIENT_REFERENCES.add(payload.clientReference)

    # Generate a mock transaction ID for successful payments
    transaction_id = generate_transaction_id()

    return PaymentResponse(
        status="SUCCESS",
        errorCode=None,
        transactionId=transaction_id,
        message="Payment processed successfully."
    )