from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class MovimentoTipo(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class EstoqueMovimento(Base):
    __tablename__ = "estoque_movimentos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(Enum(MovimentoTipo), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    produto = relationship("Produto", backref="movimentacoes")
