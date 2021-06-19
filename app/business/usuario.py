import requests, json, os, jwt
from datetime import datetime, timedelta
from flask import jsonify, current_app
from app.models.usuario import Usuario
from app.models.token_invalido import TokenInvalido
from flask_restplus import abort
from app import db


def usuario_totos():
    return Usuario.query.all() 

def usuario_por_id(id_bd):
    return Usuario.query.filter_by(id=id_bd).first()

def usuario_por_email(email_bd):
    return Usuario.query.filter_by(email=email_bd).first()


def usuario_por_token(request_headers):
    token = None
    token = request_headers['Authorization']
    token_puro = token.replace('JWT ','')
    decoded = jwt.decode(token_puro, current_app.config.get("SECRET_KEY"), algorithms="HS256")
    usuario_bd = usuario_por_id(decoded['id'])
    return usuario_bd


def usuario_login(data):
    
    usuario_bd = Usuario.query.filter_by(email=data.get('email'), senha=data.get('senha')).first()
    if usuario_bd is None:
        abort(400, msg='Login inválido')


    token = usuario_bd.gerar_token()
    
    token_final = None
    try:
        token_final = token.decode()
    except:
        token_final = token
    
            
    return {
        'msg':'Sucesso',
        'auth':True,
        'token': token_final
    }, 200



def usuario_adicionar(data):
    if usuario_por_email(data.get('email')) is not None:
        return abort(400, msg='Usuario com esse email já existente')


    usuario_bd = Usuario(
        nome=data.get('nome'),
        senha=data.get('senha'),
        email=data.get('email'),
        admin=False,
        status=True,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
        )


    salvar_bd(usuario_bd)
    return {
        'msg':"Usuario criado com Sucesso",
    }, 201


def usuario_add_lista_token_invalido(request_headers):
    token = None
    
    if 'Authorization' in request_headers:
        token = request_headers['Authorization']
        
    if not token:
        return abort(401, erro='Essa rota necessita de um token :/')
    
    if not 'JWT' in token:
        return abort(401, erro='Token Invalido')
    
    try:
        token_puro = token.replace('JWT ','')
        token_invalido_bd = TokenInvalido(
            token=token_puro,
            token_valido=False,
            data_criacao=datetime.now().replace(microsecond=0),
            data_atualizacao=datetime.now().replace(microsecond=0)
        )

        salvar_bd(token_invalido_bd)
        return {}, 204

    except:
        return abort(401,erro='Token Invalido')





def salvar_bd(data):
    db.session.add(data)
    db.session.commit()

def remover_bd(data):
    db.session.delete(data)
    db.session.commit()