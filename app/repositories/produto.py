from sqlalchemy.orm import Session
# tabela produto
from app.models.produto import Produto
from app.models.categoria import Categoria
from fastapi import HTTPException
# contrato da API
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut

def create(db: Session, payload: ProdutoCreate) -> Produto:
    # objeto = Produto(nome=payload.nome, preco=payload.preco,categoria_id=payload.categoria_id )
    #ver se a categoria existe
    categoria_id = db.get(Categoria, payload.categoria_id)
    if not categoria_id:
        raise HTTPException(status_code=400, detail="Categoria nao existe")
    objeto = Produto(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get_by_id(db: Session, id: int) -> Produto | None:
    return db.get(Produto, produto_id)

def get_all(db: Session) -> list[Produto]:
    return db.query(Produto).order_by(Produto.id).all()