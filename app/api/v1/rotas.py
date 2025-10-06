from fastapi import APIRouter
from app.api.v1 import categoria, produto, estoque

api_rotas = APIRouter()
api_rotas.include_router(categoria.rotas)
api_rotas.include_router(produto.rotas)
api_rotas.include_router(estoque.router)