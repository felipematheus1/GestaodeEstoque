# 📦 Gestão de Estoque – API com FastAPI
 `Alunos`: Felipe de Souza Alves Matheus - RA: 007288
         Caio da Silva Melo - RA: 007206

Este projeto consiste em uma **API de gestão de estoque** desenvolvida como atividade prática para a disciplina de **Desenvolvimento de Sistemas WEB I**.

A aplicação foi construída utilizando **FastAPI** e **SQLite** como banco de dados. O sistema implementa o **CRUD** completo para **Produtos** e **Categorias**, e expande com funcionalidades robustas de **controle de estoque** e relatórios, conforme solicitado nas etapas da atividade.

---

## 🚀 Funcionalidades Implementadas

### 🔹 Produtos
O modelo `Produto` foi expandido com campos cruciais para a gestão de estoque:
- **`estoque_minimo`**: Quantidade mínima exigida em estoque.
- **`ativo`**: Flag booleana que indica se o produto está disponível para operações.

### 🔹 Movimentações de Estoque
Novo modelo **`EstoqueMovimento`** para registro detalhado das transações:
- `id, produto_id, tipo (ENTRADA/SAIDA), quantidade, motivo, criado_em`.

**Rotas Principais:**
- `POST /api/v1/estoque/movimentos`: Cria uma movimentação manual.
- `GET /api/v1/estoque/saldo/{produto_id}`: Retorna o saldo atual do produto.

### 🔹 Regras de Saldo
- **Cálculo de Saldo**: O saldo é sempre calculado dinamicamente (`entradas – saídas`) a partir do histórico de movimentações, nunca armazenado diretamente.
- **Bloqueio de Saldo Negativo**: Implementado por padrão, mas é **configurável** via variável de ambiente `ALLOW_NEGATIVE_STOCK` no arquivo `.env`.

### 🔹 Operações Compostas (Business Logic)
Rotas simplificadas para operações comuns:
- `POST /api/v1/estoque/venda`: Registra uma `SAÍDA` com o motivo `"venda"`.
- `POST /api/v1/estoque/devolucao`: Registra uma `ENTRADA` com o motivo `"devolucao"`.
- `POST /api/v1/estoque/ajuste`: Registra uma `ENTRADA` ou `SAÍDA` para ajuste de inventário (motivo obrigatório).

### 🔹 Relatórios e Consultas
- `GET /api/v1/estoque/extrato/{produto_id}?limit&offset`: Histórico detalhado de movimentações.
- `GET /api/v1/estoque/resumo`: Resumo consolidado de todos os produtos (saldo, estoque mínimo, status).
- `GET /api/v1/produtos/abaixo-minimo`: Lista de produtos cujo saldo atual está abaixo do `estoque_minimo`.

---

## ⚙️ Configuração e Execução

### **Requisitos**

- Python 3.10+
- FastAPI
- SQLAlchemy
- Uvicorn

### **Instalação**

Clone o projeto ou baixe os arquivos.

1.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```

### **Acesso à API**

Acesse as interfaces interativas no navegador:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **Redoc:** `http://127.0.0.1:8000/redoc`

---

## 🌐 Exemplos de Uso (Via Swagger)

| Operação | Rota / Dados de Exemplo |
| :--- | :--- |
| **Criar Produto** | `POST /api/v1/produtos`<br>```json\n{\n  "nome": "Camiseta Azul",\n  "descricao": "Camiseta tamanho M",\n  "preco": 50,\n  "categoria_id": 1,\n  "estoque_minimo": 5,\n  "ativo": true\n}``` |
| **Movimentação (ENTRADA)** | `POST /api/v1/estoque/movimentos`<br>```json\n{\n  "produto_id": 1,\n  "tipo": "ENTRADA",\n  "quantidade": 10,\n  "motivo": "compra_fornecedor"\n}``` |
| **Movimentação (SAÍDA)** | `POST /api/v1/estoque/movimentos`<br>```json\n{\n  "produto_id": 1,\n  "tipo": "SAIDA",\n  "quantidade": 3,\n  "motivo": "venda"\n}``` |
| **Venda (Simplificada)** | `POST /api/v1/estoque/venda?produto_id=1&quantidade=2` |
| **Devolução (Simplificada)** | `POST /api/v1/estoque/devolucao?produto_id=1&quantidade=1` |
| **Consultar Saldo** | `GET /api/v1/estoque/saldo/1`<br>_Exemplo de Resposta: `{"produto_id": 1, "saldo": 7}`_ |
| **Extrato** | `GET /api/v1/estoque/extrato/1?limit=10&offset=0` |
| **Produtos Abaixo Mínimo** | `GET /api/v1/produtos/abaixo-minimo` |

---

## 📌 Decisões Técnicas

1.  **Integridade Transacional**: Uso de `PRAGMA foreign_keys=ON` no SQLite para garantir a integridade referencial dos dados.
2.  **Cálculo de Saldo**: Saldo é sempre recalculado a partir das movimentações, garantindo a rastreabilidade e evitando inconsistências por dados redundantes.
3.  **Modelagem e Validação**: Utilização de **Schemas Pydantic** em todas as rotas para validação de dados de entrada e saída, assegurando consistência da API.

---

## 🏁 Conclusão

Todas as etapas da atividade foram atendidas, com a implementação completa da **modelagem** de produtos e movimentações, as **regras de saldo** e estoque mínimo, **operações compostas** (venda, devolução, ajuste) e **relatórios** de extrato e resumo.
