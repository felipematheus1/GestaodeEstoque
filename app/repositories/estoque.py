# app/repositories/estoque.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.estoque_movimento import EstoqueMovimento, MovimentoTipo
from app.models.produto import Produto
from app.schemas.estoque import EstoqueMovimentoCreate
from app.core.config import settings
from typing import List

def calcular_saldo(db: Session, produto_id: int) -> int:
    entradas = db.query(func.coalesce(func.sum(EstoqueMovimento.quantidade).filter(EstoqueMovimento.tipo == MovimentoTipo.ENTRADA, EstoqueMovimento.produto_id == produto_id), 0)).scalar()
    saidas = db.query(func.coalesce(func.sum(EstoqueMovimento.quantidade).filter(EstoqueMovimento.tipo == MovimentoTipo.SAIDA, EstoqueMovimento.produto_id == produto_id), 0)).scalar()
    # as consultas acima podem variar com a versão do SQLAlchemy; alternativa segura:
    # entradas = db.query(func.coalesce(func.sum(EstoqueMovimento.quantidade).label("total"))).filter(EstoqueMovimento.tipo==MovimentoTipo.ENTRADA, EstoqueMovimento.produto_id==produto_id).scalar() or 0
    # implementamos fallback abaixo:
    if entradas is None:
        entradas = db.query(func.sum(EstoqueMovimento.quantidade)).filter(EstoqueMovimento.tipo==MovimentoTipo.ENTRADA, EstoqueMovimento.produto_id==produto_id).scalar() or 0
    if saidas is None:
        saidas = db.query(func.sum(EstoqueMovimento.quantidade)).filter(EstoqueMovimento.tipo==MovimentoTipo.SAIDA, EstoqueMovimento.produto_id==produto_id).scalar() or 0
    return int(entradas) - int(saidas)

def criar_movimento(db: Session, movimento_in: EstoqueMovimentoCreate):
    # valida produto existe
    produto = db.query(Produto).filter(Produto.id == movimento_in.produto_id).first()
    if not produto:
        raise ValueError("Produto não encontrado")

    # se SAIDA, checar saldo atual
    if movimento_in.tipo == MovimentoTipo.SAIDA:
        saldo_atual = calcular_saldo(db, movimento_in.produto_id)
        novo_saldo = saldo_atual - movimento_in.quantidade
        if not settings.ALLOW_NEGATIVE_STOCK and novo_saldo < 0:
            raise ValueError("Saldo insuficiente. Operação bloquearia saldo negativo.")

    movimento = EstoqueMovimento(
        produto_id=movimento_in.produto_id,
        tipo=movimento_in.tipo,
        quantidade=movimento_in.quantidade,
        motivo=movimento_in.motivo
    )
    db.add(movimento)
    db.commit()
    db.refresh(movimento)
    return movimento

def extrato_movimentos(db: Session, produto_id: int, limit: int = 50, offset: int = 0) -> List[EstoqueMovimento]:
    q = db.query(EstoqueMovimento).filter(EstoqueMovimento.produto_id == produto_id).order_by(EstoqueMovimento.criado_em.desc()).limit(limit).offset(offset)
    return q.all()

def listar_produtos_abaixo_minimo(db: Session):
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    resultado = []
    for p in produtos:
        saldo = calcular_saldo(db, p.id)
        if saldo < (p.estoque_minimo or 0):
            resultado.append({"produto": p, "saldo": saldo})
    return resultado

def resumo_estoque(db: Session):
    produtos = db.query(Produto).all()
    resumo = []
    for p in produtos:
        saldo = calcular_saldo(db, p.id)
        resumo.append({
            "produto_id": p.id,
            "nome": p.nome,
            "saldo": saldo,
            "estoque_minimo": p.estoque_minimo or 0,
            "abaixo_minimo": saldo < (p.estoque_minimo or 0)
        })
    return resumo
