# Flask + MongoDB CRUD

CRUD completo de formulário com **Flask** e **MongoDB**.

## Estrutura do projeto

```
flask_crud/
├── app.py                  # Backend Flask (rotas + lógica)
├── requirements.txt
├── templates/
│   ├── base.html           # Layout base
│   ├── index.html          # Listagem de registros
│   └── form.html           # Formulário (criar / editar)
└── static/
    ├── css/style.css
    └── js/main.js
```

## Pré-requisitos

- Python 3.10+
- MongoDB rodando localmente na porta padrão (`27017`)

## Instalação

```bash
# 1. Clone / baixe o projeto e entre na pasta
cd flask_crud

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python app.py
```

Acesse: **http://localhost:5000**

## Variáveis de ambiente (opcional)

| Variável     | Padrão                        | Descrição                    |
|--------------|-------------------------------|------------------------------|
| `MONGO_URI`  | `mongodb://localhost:27017/`  | URI de conexão ao MongoDB    |
| `SECRET_KEY` | `sua-chave-secreta-aqui`      | Chave para sessões Flask     |

Exemplo:
```bash
export MONGO_URI="mongodb+srv://user:senha@cluster.mongodb.net/"
export SECRET_KEY="minha-chave-super-secreta"
python app.py
```

## Rotas

| Método | Rota             | Descrição                         |
|--------|------------------|-----------------------------------|
| GET    | `/`              | Lista todos os registros          |
| GET    | `/novo`          | Exibe formulário de cadastro      |
| POST   | `/novo`          | Salva novo registro               |
| GET    | `/editar/<id>`   | Exibe formulário de edição        |
| POST   | `/editar/<id>`   | Atualiza registro                 |
| POST   | `/deletar/<id>`  | Remove registro                   |
| GET    | `/api/registros` | Retorna todos os registros em JSON|

## MongoDB

- **Banco:** `crud_db`
- **Coleção:** `formulario`
- **Campos:** `nome`, `email`, `telefone`
