"""
Pruebas automatizadas del backend Sistema de Transporte (pytest + FastAPI)

Este archivo contiene 5 pruebas exitosas que demuestran:
1. Acceso a documentación OpenAPI
2. Autenticación de administrador
3. Autenticación de cliente
4. Headers de seguridad CORS (preflight)
5. Obtención de lista de clientes con token de administrador
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthAndDocumentation:
    """
    PRUEBA 1: Verificar que el endpoint de documentación OpenAPI es accesible
    
    ✅ Propósito: Confirmar que FastAPI levanta correctamente y sirve la documentación.
    - Se realiza un GET a /docs (página Swagger UI de FastAPI)
    - Se verifica que la respuesta sea 200 OK
    - Esta es una "smoke test" que verifica que la app está viva.
    """

    def test_openapi_docs_accessibility(self, client: TestClient):
        """
        Acceso a documentación OpenAPI (Swagger UI).
        
        Arrange: Preparamos el cliente de prueba (inyectado por pytest via fixture)
        Act: Realizamos GET a /docs
        Assert: Verificamos status 200
        """
        response = client.get("/docs")
        assert response.status_code == 200
        # Verificamos que es HTML de Swagger
        assert "swagger-ui" in response.text.lower()


class TestAdminAuthentication:
    """
    PRUEBA 2: Autenticación exitosa de administrador
    
    ✅ Propósito: Verificar que el endpoint de login para admin funciona correctamente.
    - Se envía documento y contraseña de admin (seeded en la BD)
    - Se verifica status 200
    - Se verifica estructura de respuesta (access_token, token_type, role)
    - Se extrae el token para usarlo en pruebas subsecuentes
    """

    def test_admin_login_with_valid_credentials(self, client: TestClient):
        """
        Login de administrador con credenciales válidas.
        
        El administrador seeded en la BD tiene:
        - documento: "1021923966"
        - contraseña: "Admin123!"
        
        Arrange: Preparamos credenciales válidas
        Act: POST a /auth/login/admin con datos
        Assert: Verificamos status 200 y estructura del token
        """
        login_data = {
            "documento": "1021923966",
            "contrasena": "Admin123!"
        }
        response = client.post("/auth/login/admin", json=login_data)
        
        # Verificar status HTTP
        assert response.status_code == 200
        
        # Parsear JSON
        body = response.json()
        
        # Verificar estructura de respuesta
        assert "access_token" in body
        assert "token_type" in body
        assert "expires_in" in body
        assert "role" in body
        
        # Verificar valores específicos
        assert body["token_type"] == "bearer"
        assert body["role"] == "admin"
        assert body["expires_in"] > 0
        assert isinstance(body["access_token"], str)
        assert len(body["access_token"]) > 0


class TestClientAuthentication:
    """
    PRUEBA 3: Autenticación exitosa de cliente
    
    ✅ Propósito: Verificar que el endpoint de login para cliente funciona correctamente.
    - Se envía documento y contraseña de cliente (seeded en la BD)
    - Se verifica status 200
    - Se verifica estructura de respuesta similar a admin
    - Se confirma que el role es "cliente" (diferente de admin)
    """

    def test_client_login_with_valid_credentials(self, client: TestClient):
        """
        Login de cliente con credenciales válidas.
        
        El cliente seeded en la BD tiene:
        - documento: "12345678"
        - contraseña: "cliente_seguro123"
        
        Arrange: Preparamos credenciales válidas de cliente
        Act: POST a /auth/login/cliente con datos
        Assert: Verificamos status 200 y role correcto
        """
        login_data = {
            "documento": "12345678",
            "contrasena": "cliente_seguro123"
        }
        response = client.post("/auth/login/cliente", json=login_data)
        
        # Verificar status HTTP
        assert response.status_code == 200
        
        # Parsear JSON
        body = response.json()
        
        # Verificar estructura (igual que admin)
        assert "access_token" in body
        assert "token_type" in body
        assert "expires_in" in body
        assert "role" in body
        
        # Verificar que el role es "cliente" (no admin)
        assert body["role"] == "cliente"
        assert body["token_type"] == "bearer"
        
        # Verificar que el token no esté vacío
        assert len(body["access_token"]) > 0


class TestCORSHeaders:
    """
    PRUEBA 4: Verificar headers de seguridad y CORS (preflight)
    
    ✅ Propósito: Confirmar que el middleware CORS está configurado correctamente.
    - Se realiza un OPTIONS request (preflight CORS que envía el navegador)
    - Se verifica que devuelve 200
    - Se verifica headers Access-Control-Allow-Origin, Access-Control-Allow-Methods, etc.
    - Esto asegura que el frontend en localhost:4200 o 5173 pueda comunicarse
    """

    def test_cors_preflight_headers_present(self, client: TestClient):
        """
        Verificar que CORS preflight permite origen localhost:4200 (frontend Angular).
        
        Arrange: Preparamos headers de preflight CORS típicos
        Act: Enviamos OPTIONS a /clientes con headers
        Assert: Verificamos que respuesta tiene headers CORS correctos
        """
        # Headers que envía el navegador en un preflight request
        headers = {
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        }
        
        response = client.options("/clientes", headers=headers)
        
        # Verificar que no es error (200 o 204 son normales en preflight)
        assert response.status_code in [200, 204]
        
        # Verificar que los headers CORS están presentes
        # (Nota: en Starlette/FastAPI son case-insensitive para lectura)
        response_headers = response.headers
        
        # Verificar que permite el origen
        assert "access-control-allow-origin" in response_headers
        assert response_headers["access-control-allow-origin"] == "http://localhost:4200"
        
        # Verificar que permite los métodos
        assert "access-control-allow-methods" in response_headers
        
        # Verificar que permite headers
        assert "access-control-allow-headers" in response_headers


class TestGetClientesWithAuth:
    """
    PRUEBA 5: Obtener lista de clientes con token de administrador
    
    ✅ Propósito: Verificar que endpoints protegidos funcionan con Bearer token.
    - Primero login de admin para obtener token
    - Luego GET a /clientes con Authorization header
    - Verifica status 200 y estructura de respuesta (lista de clientes)
    - Demuestra flujo: authenticate → get token → use token in Bearer header
    """

    def test_get_clientes_with_admin_bearer_token(self, client: TestClient):
        """
        Obtener lista de clientes usando token JWT de administrador.
        
        Este test demuestra el flujo completo:
        1. Admin login para obtener token
        2. GET /clientes con Authorization: Bearer <token>
        3. Verificar que devuelve lista de clientes
        
        Arrange: Login para obtener token de admin
        Act: GET /clientes con header Authorization
        Assert: Verificamos status 200 y estructura de lista
        """
        # STEP 1: Obtener token de admin
        login_data = {
            "documento": "1021923966",
            "contrasena": "Admin123!"
        }
        login_response = client.post("/auth/login/admin", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        
        # STEP 2: Usar token para GET /clientes
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = client.get("/clientes", headers=headers)
        
        # Verificar status 200
        assert response.status_code == 200
        
        # Verificar que es una lista
        body = response.json()
        assert isinstance(body, list)
        
        # Verificar que hay al menos un cliente (el seeded)
        assert len(body) >= 1
        
        # Verificar estructura del primer cliente
        cliente = body[0]
        assert "documento" in cliente
        assert "nombre" in cliente
        assert "email" in cliente
        assert "telefono" in cliente
        assert "direccion" in cliente
        
        # Verificar que el cliente seeded está en la lista
        cliente_seeded = next(
            (c for c in body if c["documento"] == "12345678"), 
            None
        )
        assert cliente_seeded is not None
        assert cliente_seeded["nombre"] == "Juan Perez"
