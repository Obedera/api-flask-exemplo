import jwt
from app import db
from datetime import datetime, timedelta
from flask import current_app

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(128), nullable=False, index=True)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0), onupdate=datetime.now().replace(microsecond=0))


    def gerar_token(self):
        data = datetime.utcnow()
        qtde_horas_token = current_app.config.get("TOKEN_EXPIRE_HOURS")
        qtde_minutos_token = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        tempo_expiracao = data + timedelta(hours=qtde_horas_token, minutes=qtde_minutos_token)
        payload = dict(exp=tempo_expiracao, iat=data, id=self.id, admin=self.admin)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")

        