import pytest
import os
from app import create_app


@pytest.fixture(scope='session', autouse=True)
def create_obj_models():
    from app.models.usuario import Usuario
    
    from datetime import datetime, timedelta

    lista_obj = []
    usuario_bd_1 = Usuario(
        nome='Obede',
        email='obede@gmail.com',
        senha='pokemon123',
        admin=True,
        status=True,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
    )

    usuario_bd_2 = Usuario(
        nome='Obedera',
        email='obedera@gmail.com',
        senha='pokemon123',
        admin=True,
        status=True,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
    )

    usuario_bd_3 = Usuario(
        nome='Jacqueline',
        email='jacqueline@gmail.com',
        senha='pokemon123',
        admin=True,
        status=True,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
    )

    usuario_bd_4 = Usuario(
        nome='Stefani',
        email='stefani@gmail.com',
        senha='pokemon123',
        admin=True,
        status=True,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
    )

    


    lista_obj.append(usuario_bd_1)
    lista_obj.append(usuario_bd_2)
    lista_obj.append(usuario_bd_3)
    lista_obj.append(usuario_bd_4)
    
    yield lista_obj



@pytest.fixture(scope='session', autouse=True)
def init_db():
    from sqlalchemy import create_engine
    user_t = os.getenv('RDS_USERNAME_TEST')
    pw_t = os.getenv('RDS_PASSWORD_TEST')
    url_t = os.getenv('RDS_HOSTNAME_TEST')
    db_t = os.getenv('RDS_DB_NAME_TEST')
    DB_TEST = f'postgresql://{user_t}:{pw_t}@{url_t}/'
    engine = create_engine(DB_TEST)
    conn = engine.connect()
    conn.execute("commit")
    
    resp_query = conn.execute("select '1' where exists (select from pg_database where datname = '{}')".format(db_t))
    if len(resp_query.all()) == 0:
        conn.execute(f'create database {db_t}')
    else:
        conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '{}';".format(db_t))
        conn.execute(f'drop database {db_t}')
        conn.execute(f'create database {db_t}')

    conn.close()
   
    env = 'testing'
    main = create_app(env)
    main.test_client()

    yield main
    
    engine = create_engine(DB_TEST)
    conn = engine.connect()
    conn.execute("commit")
    resp_query = conn.execute("select '1' where exists (select from pg_database where datname = '{}')".format(db_t))
    if len(resp_query.all()) == 1:
        conn.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '{}';".format(db_t))
        conn.execute(f'drop database {db_t}')
    conn.close()
    

    



@pytest.fixture
def setup_test(init_db, create_obj_models):    
    with init_db.app_context():
        if os.path.isfile('app/bd_test.sqlite'):
            os.remove('app/bd_test.sqlite')
        
        from app import db

        from flask_migrate import upgrade as _upgrade
        _upgrade()

        for item in create_obj_models:
            db.session.add(item)
            db.session.commit()

        yield init_db

        db.engine.dispose()
        db.session.close()


@pytest.fixture
def app(setup_test):
    
    yield setup_test


@pytest.fixture
def client(app):
    return app.test_client()
