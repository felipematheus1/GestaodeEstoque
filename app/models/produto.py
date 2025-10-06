from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    preco = Column(Integer, nullable=True)  
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    # Novos campos requeridos pela atividade
    estoque_minimo = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, nullable=False, default=True)

    categoria = relationship("Categoria", back_populates="produtos")
    categoria = relationship("Categoria", back_populates="produtos")