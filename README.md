IPN Developer Integration Challenge — P2P Payment Request Application
Overview

This project is a mock implementation of a Person-to-Person (P2P) payment request flow for the IPN Developer Integration Challenge.

The application demonstrates how a client application captures payment details, validates user input, submits a request to an API endpoint, and displays the resulting transaction outcome.

The solution includes:

A frontend payment capture form

Client-side validation

A backend API endpoint for processing payment requests

Structured success and failure responses

Automated API tests

Technology Stack

Backend

FastAPI (Python)

Frontend

HTML

CSS

JavaScript

Validation

Pydantic

Testing

Pytest

Project Structure
ipn-p2p-challenge/
│
├── app/
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── styles.css
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── requirements.txt
└── README.md
Application Features

The application provides the following functionality:

Capture P2P payment details through a web form

Generate a client transaction reference

Perform frontend validation before submission

Submit payment requests to a mock backend API

Display transaction results clearly

Handle validation and business-rule failures consistently

Run automated tests for key scenarios

API Endpoint

Endpoint

POST /api/p2p-payment

Requests and responses are exchanged in JSON format.

Example Request Body
{
  "clientReference": "REF-1001",
  "senderAccountNumber": "1234567890",
  "receiverAccountNumber": "0987654321",
  "amount": 150.00,
  "currency": "NAD",
  "reference": "Lunch payment"
}
Successful Response
{
  "status": "SUCCESS",
  "errorCode": null,
  "transactionId": "TXN-20260314-ABC12345",
  "message": "Payment processed successfully."
}
Failed Response Example
{
  "status": "FAILED",
  "errorCode": "ERR005",
  "transactionId": null,
  "message": "Insufficient funds."
}
Validation Rules

The application enforces the following validation rules:

clientReference

Required

Must be unique per transaction

senderAccountNumber

Numeric only

Minimum length: 10

receiverAccountNumber

Numeric only

Minimum length: 10

Account numbers

Sender and receiver must be different

amount

Must be greater than 0

currency

Must equal NAD

reference

Must not be empty

Maximum length: 50 characters

Business Rules / Simulation

Because the challenge does not involve a real payment system, several rules simulate payment outcomes.

Duplicate Client Reference

If the same clientReference is submitted more than once, the transaction fails with:

ERR001 – Duplicate client reference
Insufficient Funds Simulation

To simulate insufficient funds:

amount > 5000.00

returns:

ERR005 – Insufficient funds
Internal Processing Error Simulation

If the payment reference contains the word "error", the request returns:

ERR006 – Internal processing error

This allows testing of server-side failure scenarios.

Assumptions

The challenge allows reasonable assumptions where integration details are not specified.

The following assumptions were made:

The API endpoint is implemented locally for simulation purposes

Duplicate client references are tracked in memory during the application session

Amounts greater than NAD 5000.00 simulate insufficient funds

A payment reference containing the word "error" simulates an internal processing failure

Transaction IDs are generated locally for successful payments

The following items are intentionally excluded as they are outside the challenge scope:

Database persistence

Authentication or authorization

Encryption or message signing

Integration with live IPN systems

Setup Instructions
1. Create a virtual environment
python -m venv venv
2. Activate the virtual environment

Windows CMD

venv\Scripts\activate

PowerShell

venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Run the application
uvicorn app.main:app --reload
5. Open the application
http://127.0.0.1:8000
6. API Documentation

FastAPI provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs
Running Tests

Automated tests are implemented using pytest.

Run tests with:

python -m pytest
Testing Coverage

The automated tests cover the following scenarios:

Successful payment processing

Duplicate client reference rejection

Insufficient funds simulation

Internal processing error simulation

Validation failure for identical sender and receiver accounts

Validation failure for unsupported currency

Design Notes

The solution was intentionally kept simple but structured to reflect good engineering practices:

Clear separation between frontend and backend responsibilities

Explicit validation rules using Pydantic

Structured error handling

Reusable helper functions for payment responses

Deterministic simulation rules for negative-path testing

Automated tests for both success and failure scenarios

Possible Production Enhancements

If extended into a production-ready system, the following improvements would be recommended:

Persistent storage for transactions and client references

Authentication and authorization mechanisms

Audit logging and correlation IDs

Integration with external payment rails or banking systems

Secure secret management

Retry and circuit-breaker patterns for downstream services

CI/CD pipeline automation

Monitoring and alerting

