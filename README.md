Rodar a Aplicação

- python3 -m venv .venv
- source .venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt
- source .env
- flask run

Rodar no Docker
docker build -t api-flask-exemplo . && docker run -p 8000:8000 --env-file .env api-flask-exemplo

Rodar Testes
- source .venv/bin/activate
- source .env
- pytest

Comandos BD Flask
- flask db init
- flask db migrate -m "<nome-alteração>" - Gravar alteração no migrations
- flask db upgrade -  realizar migrações no BD


Doc
- http://localhost:5000/api-flask-exemplo/v1/ui


