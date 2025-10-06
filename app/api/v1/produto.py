from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.produto import ProdutoCreate, ProdutoOut
from app.repositories import produto as repo

rotas = APIRouter(prefix="/v1/produto", tags=["produto"])

@rotas.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED) 
def create(payload: ProdutoCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload)

@rotas.get("/", response_model=list[ProdutoOut])
def list_all(db: Session = Depends(get_db)):
    return repo.get_all(db)

@rotas.get("/", response_model=ProdutoOut)
def get_id(produto_id: int, db: Session = Depends(get_db)):
    objeto = repo.get(db, produto_id)
    if not objeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrada"
        )
    return objeto

