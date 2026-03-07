import random
import uuid

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from src.database.config import Base, SessionLocal


class Tarjeta(Base):
    __tablename__ = "tarjetas"
    id = Column(String(36),  index=True, default=lambda: str(uuid.uuid4()))
    numero_tarjeta = Column(
        String(16),
        primary_key=True,
        index=True,
        default=lambda: Tarjeta.encontrar_numero(),
    )
    documento_cliente = Column(
        String,
        ForeignKey("clientes.documento",ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    saldo = Column(Integer, nullable=False,default=0)

    cliente = relationship("Cliente", back_populates="tarjeta")
    
    @staticmethod
    def encontrar_numero() -> str:
        while True:
            numero = ""
            for _ in range(16):
                numero += str(random.randint(0, 9))

            db = SessionLocal()
            try:
                existe = (
                    db.query(Tarjeta)
                    .filter(Tarjeta.numero_tarjeta == numero)
                    .first()
                )
            finally:
                db.close()

            if not existe:
                return numero
