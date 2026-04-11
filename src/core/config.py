import os


JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def get_jwt_secret_key() -> str:
	"""Obtiene la clave secreta JWT desde variables de entorno."""
	secret = os.getenv("JWT_SECRET_KEY")
	if not secret:
		raise RuntimeError("JWT_SECRET_KEY no está configurada. Define esta variable en tu entorno o en .env.")
	return secret
