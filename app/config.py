import os
from pathlib import Path


APP_ROOT = Path(__file__).parent
user = os.getenv('RDS_USERNAME')
pw = os.getenv('RDS_PASSWORD')
url = os.getenv('RDS_HOSTNAME')
db = os.getenv('RDS_DB_NAME')
DB_HOST = f'postgresql://{user}:{pw}@{url}/{db}'
'''
Sqlite
DB_TEST = "sqlite:///" + str(APP_ROOT / "bd_test.sqlite")
'''
user_t = os.getenv('RDS_USERNAME_TEST')
pw_t = os.getenv('RDS_PASSWORD_TEST')
url_t = os.getenv('RDS_HOSTNAME_TEST')
db_t = os.getenv('RDS_DB_NAME_TEST')
DB_TEST = f'postgresql://{user_t}:{pw_t}@{url_t}/{db_t}'

SECRET_KEY_API = os.getenv('SECRET_KEY_API')

BASE_URL = os.getenv('BASE_URL')

class Config:
    """Base configuration."""
    ORIGINS = ["*"]

    SECRET_KEY = SECRET_KEY_API
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = DB_HOST

class DevelopmentConfig(Config):
    """Configuração de Desenvolvimento"""
    TOKEN_EXPIRE_MINUTES = 15


class ProductionConfig(Config):
    """Configuração de Produção"""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class TestConfig(Config):
    """Configuração de Teste"""
    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = DB_TEST

ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig,
    testing=TestConfig,
    production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)