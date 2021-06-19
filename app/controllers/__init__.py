from flask import Blueprint, request
from flask_restplus import Api
from flask_restplus.apidoc import ui_for
from werkzeug.utils import cached_property

from app.controllers.usuario.usuario import api as ns_usuario


api_bp = Blueprint("api", __name__, url_prefix="/api-flask-exemplo/v1")

auth_swagger = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API Exemplo",
    description="Swagger UI documentation Api!",
    doc='/ui',
    security='Bearer Auth',
    authorizations=auth_swagger
)


api.add_namespace(ns_usuario, path="/usuario")