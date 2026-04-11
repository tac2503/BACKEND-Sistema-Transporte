from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
response = client.get("/docs")
assert response.status_code == 200
print("Smoke test OK - documentacion accessible")
