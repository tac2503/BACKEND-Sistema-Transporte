$env:PYTHONPATH = "D:\BACKEND-Sistema-Transporte"
&"D:\BACKEND-Sistema-Transporte\venv\Scripts\python.exe" -c "from fastapi.testclient import TestClient; from app import app; client = TestClient(app); resp = client.get('/docs'); print(f'Status: {resp.status_code}'); assert resp.status_code == 200; print('Smoke test OK')"
