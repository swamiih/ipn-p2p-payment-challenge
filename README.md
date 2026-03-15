# IPN Developer Integration Challenge — P2P Payment Request Application

## Overview
This project is a mock implementation of a Person-to-Person (P2P) payment request flow for the IPN Developer Integration Challenge.

The solution provides:
- a frontend payment capture form
- client-side validation
- a backend API endpoint for processing payment requests
- structured success and failure responses
- automated API tests

---

## Technology Stack
- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Validation:** Pydantic
- **Testing:** Pytest

---

## Project Structure
```text
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
│   └── test_api.py
│
├── requirements.txt
└── README.md


Features

Capture P2P payment details through a web form

Generate a client reference automatically

Perform frontend validation before submission

Submit payment requests to a mock backend API

Display transaction results clearly

Handle validation and business-rule failures consistently

Run automated tests for key scenarios

API Endpoint

POST /api/p2p-payment

Request Body
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

The following validation rules are enforced:

clientReference is required

senderAccountNumber must be numeric and at least 10 digits

receiverAccountNumber must be numeric and at least 10 digits

sender and receiver account numbers must be different

amount must be greater than 0

currency must be NAD

reference must not be empty and must not exceed 50 characters


Business Rules / Simulations

The following business rules were implemented for the mock processing flow:

Duplicate client reference

If the same clientReference is submitted again, the request fails with ERR001.

Insufficient funds simulation

If amount > 5000.00, the request fails with ERR005.

Internal processing error simulation

If the payment reference contains the word error, the request fails with ERR006.


Assumptions Made

The challenge allows reasonable assumptions because external live integration is out of scope.

The following assumptions were applied:

Duplicate client references are rejected within the current application session.

Amounts greater than NAD 5000.00 simulate insufficient funds.

A payment reference containing the word "error" simulates an internal processing failure.

Transaction IDs are generated locally for mock processing.

Database persistence, authentication, encryption, and live IPN integration are intentionally excluded as they are outside the challenge scope


How to Run the Application

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

5. Open in browser
http://127.0.0.1:8000

6. Open API docs
http://127.0.0.1:8000/docs


How to Run Tests
Bash
python -m pytest


Design Notes

This solution was intentionally kept simple, but structured in a way that reflects good engineering practice:

clear separation between frontend and backend responsibilities

explicit validation rules using Pydantic

structured error handling

reusable helper functions for payment processing responses

deterministic simulation rules for negative-path testing

automated tests for both success and failure scenarios



Possible Production Enhancements

If this were extended into a production-ready system, the following improvements would be recommended:

persistent storage for transactions and client references

proper authentication and authorization

audit logging and correlation IDs

integration with external payment rails or bank services

secure secret management

retry and circuit-breaker patterns for downstream service calls

CI/CD pipeline automation

monitoring and alerting


## Testing Coverage

The following scenarios are covered by automated tests:

- Successful payment processing
- Duplicate client reference rejection
- Insufficient funds simulation
- Internal processing error simulation
- Validation failure for identical sender and receiver accounts
- Validation failure for unsupported currency

Tests are implemented using **pytest** and executed using:
python -m pytest
