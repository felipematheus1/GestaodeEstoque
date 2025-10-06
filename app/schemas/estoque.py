# app/schemas/estoque.py
from pydantic import BaseModel, Field, conint
from typing import Optional
from datetime import datetime
from enum import Enum

class MovimentoTipo(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class EstoqueMovimentoCreate(BaseModel):
    produto_id: int
    tipo: MovimentoTipo
    quantidade: conint(gt=0)
    motivo: Optional[str] = None

class EstoqueMovimentoOut(BaseModel):
    id: int
    produto_id: int
    tipo: MovimentoTipo
    quantidade: int
    motivo: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True

class SaldoOut(BaseModel):
    produto_id: int
    saldo: int

class ResumoEstoqueOut(BaseModel):
    produto_id: int
    nome: str
    saldo: int
    estoque_minimo: int
    abaixo_minimo: bool
