from flask import request
from flask_restplus import Resource
from app.business.usuario import usuario_adicionar, usuario_login, usuario_por_id, usuario_totos, usuario_add_lista_token_invalido, usuario_por_token
from app.controllers.usuario.usuario_dto import Usuario_DTO
from app.util.auth import jwt_required, jwt_required_admin


api = Usuario_DTO.ns_user
_login_dto = Usuario_DTO.login_usuario_dto
_cadastrar_usuario_dto = Usuario_DTO.cadastrar_usuario_dto
_recuperar_dto = Usuario_DTO.recuperar_usuario_dto
_response_usuario_dto = Usuario_DTO.response_usuario_dto

@api.route('/cadastrar')
class UsuarioCadastrar(Resource):
    
    @api.expect(_cadastrar_usuario_dto, validate=True)
    def post(self):
        return usuario_adicionar(request.json)

@api.route('/login')
class UsuarioLogin(Resource):

    @api.expect(_login_dto, validate=True)
    def post(self):
        return usuario_login(request.json)


@api.route('/logout')
class UsuarioLogin(Resource):

    def delete(self):
        return usuario_add_lista_token_invalido(request.headers)


@api.route('/')
class UsuarioLista(Resource):

    @jwt_required_admin
    @api.marshal_list_with(_response_usuario_dto)
    def get(self):
        return usuario_totos()


@api.route('/token/dados')
class UsuarioToken(Resource):

    @jwt_required
    @api.marshal_with(_response_usuario_dto)
    def get(self):
        return usuario_por_token(request.headers)

@api.route('/token/check')
class UsuarioTokenCheck(Resource):

    @jwt_required
    def get(self):
        return {'msg': 'Token valido'}, 200

