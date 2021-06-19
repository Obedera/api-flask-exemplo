from flask_restplus import Namespace
from flask_restplus.fields import String, Integer, Boolean, DateTime


class Usuario_DTO:
    ns_user = Namespace('usuario', validate=True)

    login_usuario_dto = ns_user.model('Usuario Login',{
        "email": String(required=True),
        "senha": String(required=True)
    })

    cadastrar_usuario_dto = ns_user.model('Usuario Cadastro',{
        "nome": String(required=True),
        "email":String(required=True),
        "senha": String(required=True)
    })

    recuperar_usuario_dto = ns_user.model('Usuario Recuperar',{
        "email":String(required=True)
    })


    response_usuario_dto = ns_user.model('Usuario Dados Token',{
        "id": Integer,
        "nome": String,
        "email": String,
        "admin": Boolean,
        "status": Boolean,
        "data_criacao": DateTime,
        "data_atualizacao": DateTime
    })