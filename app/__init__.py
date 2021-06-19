import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import get_config
from werkzeug.middleware.proxy_fix import ProxyFix

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()




def create_app(config_name):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    @app.route("/api-flask-exemplo/")
    def index():
        return jsonify({'msg':f'Funcionando {datetime.now()}'})

    app.config.from_object(get_config(config_name))

    from app.controllers import api_bp

    app.register_blueprint(api_bp)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


    return app