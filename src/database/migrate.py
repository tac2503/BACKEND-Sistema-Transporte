from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

import src.models  # noqa: F401
from src.database.config import engine, create_tables

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"

load_dotenv()


def ensure_migrations_table(conn):

    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS _schema_migrations (
                name VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    )
    conn.commit()


def applied_migrations(conn):
    r = conn.execute(text("SELECT name FROM _schema_migrations"))
    return {row[0] for row in r}


def run_sql_file(conn, path: Path):
    sql = path.read_text(encoding="utf-8")

    statements = [
        s.strip()
        for s in sql.split(";")
        if s.strip() and not s.strip().startswith("--")
    ]

    for stmt in statements:
        if stmt:
            conn.execute(text(stmt))
    conn.commit()


def run_pending_migrations(conn):
    if not MIGRATIONS_DIR.is_dir():
        return
    applied = applied_migrations(conn)
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for f in files:
        name = f.name
        if name in applied:
            continue
        print(f"Aplicando migracion: {name}")
        run_sql_file(conn, f)
        conn.execute(
            text("INSERT INTO _schema_migrations (name) VALUES (:name)"), {"name": name}
        )
        applied.add(name)
    conn.commit()


def main():
    try:
        print("Creando / actualizando tablas desde modelos...")
        create_tables()

        with engine.connect() as conn:
            ensure_migrations_table(conn)
            print("Ejecutando migraciones pendientes...")
            run_pending_migrations(conn)

        print("Migraciones aplicadas exitosamente.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print(
                "Error: fallo de autenticación con la BD. Revisa DATABASE_URL en .env"
            )
        else:
            print("Error de conexion a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
