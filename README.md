# API de Tarefas - Projeto 3

API REST de tarefas pessoais construída com Django REST Framework. O login usa
Token Authentication e cada usuário só consegue consultar, alterar ou remover
as próprias tarefas.

## Como rodar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O SQLite é usado por padrão em `db.sqlite3`. O arquivo não deve ser enviado ao
GitHub. Para administração, acesse `http://127.0.0.1:8000/admin/`.
Ao abrir `http://127.0.0.1:8000/`, a API exibe seu status de funcionamento.

## Endpoints

| Método | URL | Ação |
|---|---|---|
| POST | `/api/login/` | Obtém um token |
| GET | `/api/tarefas/` | Lista as tarefas do usuário |
| POST | `/api/tarefas/` | Cria uma tarefa |
| GET | `/api/tarefas/<id>/` | Consulta uma tarefa própria |
| PUT/PATCH | `/api/tarefas/<id>/` | Atualiza uma tarefa própria |
| DELETE | `/api/tarefas/<id>/` | Remove uma tarefa própria |

Use `Authorization: Token <token>` nas rotas protegidas. A listagem aceita
`?concluida=true|false` e `?prioridade=alta|media|baixa`.

## Exemplos

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/login/ -d "username=ana&password=senha123"
curl.exe http://127.0.0.1:8000/api/tarefas/ -H "Authorization: Token SEU_TOKEN"
curl.exe -X POST http://127.0.0.1:8000/api/tarefas/ `
  -H "Authorization: Token SEU_TOKEN" -H "Content-Type: application/json" `
  -d '{\"titulo\":\"Estudar DRF\",\"prioridade\":\"ALTA\"}'
```

O login responde `{"token":"..."}`. A criação responde `201` e define
`usuario` pelo token, ignorando qualquer `usuario` enviado pelo cliente.
Requisições sem token respondem `401`; acessar o ID de tarefa de outra conta
responde `404`.

## Testes

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test
```

O conjunto automatizado cobre login, `401`, isolamento, filtros, criação,
PATCH e DELETE.

## Publicação

Antes de publicar, confirme que o repositório contém README, requirements e
`.gitignore`, mas não contém `venv/`, `db.sqlite3`, `.env`, tokens ou senhas.
Os comandos usuais são:

```powershell
git init
git add .
git commit -m "Projeto 3: API de Tarefas"
git branch -M main
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

Altere `SECRET_KEY`, desligue `DEBUG` e configure banco e secrets por variáveis
de ambiente antes de um deploy real.

## Autor

Seu nome - IESB 2026
