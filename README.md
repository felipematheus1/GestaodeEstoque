📦 Gestão de Estoque – FastAPI

Este projeto foi desenvolvido como atividade prática de Desenvolvimento de Sistemas WEB I.
A aplicação consiste em uma API de gestão de estoque, construída em FastAPI com SQLite como banco de dados.

O sistema expande o CRUD de Produtos e Categorias com funcionalidades completas de controle de estoque, seguindo as etapas solicitadas na atividade.

🚀 Funcionalidades Implementadas

🔹 Produtos

Campos adicionais:

estoque_minimo → quantidade mínima exigida.

ativo → indica se o produto está ativo.

🔹 Movimentações de Estoque

Novo modelo EstoqueMovimento:

id, produto_id, tipo (ENTRADA/SAIDA), quantidade, motivo, criado_em.

Rotas:

POST /api/v1/estoque/movimentos → cria uma movimentação.

GET /api/v1/estoque/saldo/{produto_id} → mostra o saldo atual.

🔹 Regras de Saldo

Saldo é sempre calculado: entradas – saídas.

Bloqueio de saldo negativo (por padrão).

Configurável via variável ALLOW_NEGATIVE_STOCK em .env.

🔹 Operações Compostas

POST /api/v1/estoque/venda → registra SAÍDA com motivo "venda".

POST /api/v1/estoque/devolucao → registra ENTRADA com motivo "devolucao".

POST /api/v1/estoque/ajuste → registra ENTRADA ou SAÍDA, com motivo obrigatório.

🔹 Relatórios

GET /api/v1/estoque/extrato/{produto_id}?limit&offset → histórico de movimentações.

GET /api/v1/estoque/resumo → resumo de todos os produtos (saldo, estoque mínimo, status).

GET /api/v1/produtos/abaixo-minimo → lista produtos abaixo do estoque mínimo.

⚙️ Requisitos

Python 3.10+

FastAPI

SQLAlchemy

Uvicorn

Instale as dependências:

pip install -r requirements.txt

▶️ Como Executar

Clone o projeto ou baixe os arquivos.

Crie e ative o ambiente virtual:

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac


Instale as dependências.

Rode a aplicação:

uvicorn app.main:app --reload


Acesse no navegador:

Swagger: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

🌐 Exemplos de Uso (via Swagger)
1) Criar Produto
{
  "nome": "Camiseta Azul",
  "descricao": "Camiseta tamanho M",
  "preco": 50,
  "categoria_id": 1,
  "estoque_minimo": 5,
  "ativo": true
}

2) Criar Movimentação de Estoque (ENTRADA)
{
  "produto_id": 1,
  "tipo": "ENTRADA",
  "quantidade": 10,
  "motivo": "compra_fornecedor"
}

3) Criar Movimentação de Estoque (SAÍDA)
{
  "produto_id": 1,
  "tipo": "SAIDA",
  "quantidade": 3,
  "motivo": "venda"
}

4) Consultar Saldo

GET /api/v1/estoque/saldo/1

Resposta:

{
  "produto_id": 1,
  "saldo": 7
}

5) Venda

POST /api/v1/estoque/venda?produto_id=1&quantidade=2

6) Devolução

POST /api/v1/estoque/devolucao?produto_id=1&quantidade=1

7) Ajuste

POST /api/v1/estoque/ajuste

{
  "produto_id": 1,
  "tipo": "SAIDA",
  "quantidade": 1,
  "motivo": "perda"
}

8) Produtos abaixo do mínimo

GET /api/v1/produtos/abaixo-minimo

9) Extrato de Movimentações

GET /api/v1/estoque/extrato/1?limit=10&offset=0

10) Resumo de Estoque

GET /api/v1/estoque/resumo

📌 Decisões Técnicas

Saldo sempre recalculado a partir das movimentações, nunca gravado direto.

Bloqueio de saldo negativo implementado (padrão: não permite).

SQLite com PRAGMA foreign_keys=ON para garantir integridade.

Schemas Pydantic usados em todas as rotas para consistência.

🏁 Conclusão

Todas as etapas da atividade foram atendidas:

Modelagem de produto e movimentações.

Regras de saldo e estoque mínimo.

Operações compostas (venda, devolução, ajuste).

Relatórios (extrato e resumo).

Boas práticas implementadas.
