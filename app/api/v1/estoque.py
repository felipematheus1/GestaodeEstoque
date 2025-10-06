# app/api/v1/estoque.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.deps import get_db  # ajuste se o get_db estiver em outro local
from app.schemas.estoque import (
    EstoqueMovimentoCreate,
    EstoqueMovimentoOut,
    SaldoOut,
    ResumoEstoqueOut
)
from app.repositories import estoque as estoque_repo
from app.models.estoque_movimento import MovimentoTipo
from app.core.config import settings

router = APIRouter(prefix="/api/v1/estoque", tags=["estoque"])

@router.post("/movimentos", response_model=EstoqueMovimentoOut)
def criar_movimento(movimento_in: EstoqueMovimentoCreate, db: Session = Depends(get_db)):
    try:
        mov = estoque_repo.criar_movimento(db, movimento_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return mov

@router.get("/saldo/{produto_id}", response_model=SaldoOut)
def obter_saldo(produto_id: int, db: Session = Depends(get_db)):
    # valida produto existe (reaproveitar repositório)
    from app.models.produto import Produto
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    saldo = estoque_repo.calcular_saldo(db, produto_id)
    return {"produto_id": produto_id, "saldo": saldo}

@router.post("/venda", response_model=EstoqueMovimentoOut)
def registrar_venda(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    payload = EstoqueMovimentoCreate(produto_id=produto_id, tipo=MovimentoTipo.SAIDA, quantidade=quantidade, motivo="venda")
    try:
        mov = estoque_repo.criar_movimento(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return mov

@router.post("/devolucao", response_model=EstoqueMovimentoOut)
def registrar_devolucao(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    payload = EstoqueMovimentoCreate(produto_id=produto_id, tipo=MovimentoTipo.ENTRADA, quantidade=quantidade, motivo="devolucao")
    try:
        mov = estoque_repo.criar_movimento(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return mov

@router.post("/ajuste", response_model=EstoqueMovimentoOut)
def registrar_ajuste(movimento_in: EstoqueMovimentoCreate, db: Session = Depends(get_db)):
    if not movimento_in.motivo:
        raise HTTPException(status_code=400, detail="Motivo é obrigatório para ajuste")
    try:
        mov = estoque_repo.criar_movimento(db, movimento_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return mov

@router.get("/extrato/{produto_id}", response_model=List[EstoqueMovimentoOut])
def extrato(produto_id: int, limit: int = Query(50, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    # valida produto existe
    from app.models.produto import Produto
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    movimentos = estoque_repo.extrato_movimentos(db, produto_id, limit=limit, offset=offset)
    return movimentos

@router.get("/resumo", response_model=List[ResumoEstoqueOut])
def resumo(db: Session = Depends(get_db)):
    resumo = estoque_repo.resumo_estoque(db)
    return resumo

@router.get("/produtos/abaixo-minimo", response_model=List[ResumoEstoqueOut])
def produtos_abaixo_minimo(db: Session = Depends(get_db)):
    resumo = estoque_repo.resumo_estoque(db)
    # filtrar abaixo_minimo
    abaixo = [r for r in resumo if r["abaixo_minimo"]]
    # mapear para ResumoEstoqueOut
    return [
        {
            "produto_id": r["produto_id"],
            "nome": r["nome"],
            "saldo": r["saldo"],
            "estoque_minimo": r["estoque_minimo"],
            "abaixo_minimo": r["abaixo_minimo"]
        } for r in abaixo
    ]
