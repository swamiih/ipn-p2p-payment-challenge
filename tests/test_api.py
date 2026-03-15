from fastapi.testclient import TestClient
from app.main import app, USED_CLIENT_REFERENCES

client = TestClient(app)


def setup_function():
    USED_CLIENT_REFERENCES.clear()


def test_successful_payment():
    payload = {
        "clientReference": "REF-TEST-001",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "0987654321",
        "amount": 150.00,
        "currency": "NAD",
        "reference": "Lunch payment"
    }

    response = client.post("/api/p2p-payment", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "SUCCESS"
    assert body["errorCode"] is None
    assert body["transactionId"] is not None
    assert body["message"] == "Payment processed successfully."


def test_duplicate_client_reference():
    payload = {
        "clientReference": "REF-DUP-001",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "0987654321",
        "amount": 150.00,
        "currency": "NAD",
        "reference": "Lunch payment"
    }

    first_response = client.post("/api/p2p-payment", json=payload)
    second_response = client.post("/api/p2p-payment", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409

    body = second_response.json()
    assert body["status"] == "FAILED"
    assert body["errorCode"] == "ERR001"
    assert body["message"] == "Duplicate client reference."


def test_insufficient_funds():
    payload = {
        "clientReference": "REF-TEST-002",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "0987654321",
        "amount": 7000.00,
        "currency": "NAD",
        "reference": "Large transfer"
    }

    response = client.post("/api/p2p-payment", json=payload)

    assert response.status_code == 402
    body = response.json()
    assert body["status"] == "FAILED"
    assert body["errorCode"] == "ERR005"
    assert body["message"] == "Insufficient funds."


def test_internal_processing_error():
    payload = {
        "clientReference": "REF-TEST-003",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "0987654321",
        "amount": 100.00,
        "currency": "NAD",
        "reference": "trigger error"
    }

    response = client.post("/api/p2p-payment", json=payload)

    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "FAILED"
    assert body["errorCode"] == "ERR006"
    assert body["message"] == "Internal processing error."


def test_same_sender_and_receiver_fails_validation():
    payload = {
        "clientReference": "REF-TEST-004",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "1234567890",
        "amount": 100.00,
        "currency": "NAD",
        "reference": "Same account"
    }

    response = client.post("/api/p2p-payment", json=payload)

    assert response.status_code == 422


def test_invalid_currency_fails_validation():
    payload = {
        "clientReference": "REF-TEST-005",
        "senderAccountNumber": "1234567890",
        "receiverAccountNumber": "0987654321",
        "amount": 100.00,
        "currency": "USD",
        "reference": "Wrong currency"
    }

    response = client.post("/api/p2p-payment", json=payload)

    assert response.status_code == 422