import jwt
from functools import wraps
from flask import current_app, request
from app.models.usuario import Usuario
from app.models.token_invalido import TokenInvalido

def jwt_required(f):
    wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return {'Erro': 'Essa rota necessita de um token :/'}, 401
        
        if not 'JWT' in token:
            return {'Erro': 'Token Invalido'}, 401
        
        try:
            token_puro = token.replace('JWT ','')
            token_invalido = TokenInvalido.query.filter_by(token=token_puro).first()
            if token_invalido is not None:
                return {'Erro': 'Token Invalido'}, 401



            decoded = jwt.decode(token_puro, current_app.config.get("SECRET_KEY"), algorithms="HS256")
            current_user = Usuario.query.get(decoded['id'])
        except:
            return {'Erro': 'Token Invalido'}, 401

        

        return f(*args, **kwargs)
    
    return wrapper


def jwt_required_admin(f):
    wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return {'Erro': 'Essa rota necessita de um token :/'}, 401
        
        if not 'JWT' in token:
            return {'Erro': 'Token Invalido'}, 401
        
        try:
            token_puro = token.replace('JWT ','')
            token_invalido = TokenInvalido.query.filter_by(token=token_puro).first()
            if token_invalido is not None:
                return {'Erro': 'Token Invalido'}, 401

                
            decoded = jwt.decode(token_puro, current_app.config.get("SECRET_KEY"), algorithms="HS256")
            
            if decoded['admin'] != True:
                return {'Erro': 'Token Invalido'}, 401
            
            current_user = Usuario.query.get(decoded['id'])
            
        except:
            return {'Erro': 'Token Invalido'}, 401

        

        return f(*args, **kwargs)
    
    return wrapper
