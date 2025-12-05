# ClassFocus

Aplicação Flask para gerenciamento de prazos (tarefas) com autenticação e banco MySQL.

## Características

- Banco de dados MySQL com SQLAlchemy
- Autenticação com Flask-Login (cadastro e login)
- CRUD completo (criar, listar, editar, excluir tarefas)
- Migrações com Flask-Migrate
- Criação automática do banco de dados

## Instalação rápida (Windows PowerShell)

### 1) Criar virtualenv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Instalar dependências
```powershell
pip install -r requirements.txt
```

### 3) Configurar banco de dados

Defina `DATABASE_URL` (substitua as credenciais):
```powershell
$env:DATABASE_URL = 'mysql+pymysql://root:password@localhost:3306/classfocus'
```

### 4) Criar tabelas
```powershell
$env:FLASK_APP = 'app.py'
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5) Rodar
```powershell
python app.py
```

Acesse `http://localhost:5000`

## Fluxo de uso

1. Cadastre-se em `/cadastro`
2. Faça login com seu e-mail e senha
3. Na página inicial, veja todas as tarefas
4. Crie novas tarefas em `/novo`
5. Edite ou exclua tarefas existentes
6. Filtre por disciplina clicando nas tags
7. Faça logout clicando em "Sair"

## Estrutura

- `app.py` - Rotas Flask (cadastro, login, CRUD)
- `models.py` - Modelos SQLAlchemy (User, Tarefa)
- `templates/` - Templates HTML
- `requirements.txt` - Dependências
