import jwt
from app import db
from datetime import datetime, timedelta
from flask import current_app

class TokenInvalido(db.Model):
    __tablename__ = "token_invalido"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.Text, nullable=False, index=True)
    token_valido = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0), onupdate=datetime.now().replace(microsecond=0))
        