import json


def test_usuario_adicionar(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'nome':'Obede Silva',
        'email':'obede.silva@gmail.com',
        'senha':'pokemon123'
    }

    url = '/api-flask-exemplo/v1/usuario/cadastrar'

    res = client.post(url, data=json.dumps(data), headers=headers)

    assert res.mimetype == mimetype
    assert res.status_code == 201
    assert res.json['msg'] == 'Usuario criado com Sucesso'
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(email='obede.silva@gmail.com').first()
        assert usuario_bd is not None


def test_usuario_add_duplicado_email(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'nome':'Obedera',
        'email':'obede@gmail.com',
        'senha':'pokemon123'
    }

    url = '/api-flask-exemplo/v1/usuario/cadastrar'

    res = client.post(url, data=json.dumps(data), headers=headers)
    assert res.mimetype == mimetype
    assert res.status_code == 400
    assert res.json['msg'] == 'Usuario com esse email já existente'


def test_usuario_add_faltando_dados(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'nome':'Obedera',
        'email':'obede.silva@gmail.com',
        'senha':'pokemon123'
    }

    url = '/api-flask-exemplo/v1/usuario/cadastrar'

    data['nome'] = None
    res = client.post(url, data=json.dumps(data), headers=headers)
    assert res.mimetype == mimetype
    assert res.status_code == 400



def test_usuario_login(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email':'obede@gmail.com',
        'senha':'pokemon123'
    }

    url = '/api-flask-exemplo/v1/usuario/login'

    res = client.post(url, data=json.dumps(data), headers=headers)

    assert res.mimetype == mimetype
    assert res.status_code == 200
    assert res.json['msg'] == 'Sucesso'
    assert res.json['auth'] == True
    assert type(res.json['token']) == str



def test_usuario_login_invalido(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email':'obede@gmail.com',
        'senha':'pokemon13'
    }

    url = '/api-flask-exemplo/v1/usuario/login'

    res = client.post(url, data=json.dumps(data), headers=headers)

    assert res.mimetype == mimetype
    assert res.status_code == 400
    assert res.json['msg'] == 'Login inválido'

def test_usuario_checar_token_valido(app, client):
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(admin=True).first()

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': f'JWT {usuario_bd.gerar_token()}'
        }

        url = '/api-flask-exemplo/v1/usuario/token/check'

        res = client.get(url, headers=headers)
        assert res.mimetype == mimetype
        assert res.status_code == 200
        assert res.json['msg'] == 'Token valido'


def test_usuario_checar_token_invalido(app, client):
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(admin=True).first()

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': f'JWT token'
        }

        url = '/api-flask-exemplo/v1/usuario/token/check'

        res = client.get(url, headers=headers)
        assert res.mimetype == mimetype
        assert res.status_code == 401


def test_usuario_lista(app, client):
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(admin=True).first()
        
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': f'JWT {usuario_bd.gerar_token()}'
        }

        url = '/api-flask-exemplo/v1/usuario/'

        res = client.get(url, headers=headers)


        assert usuario_bd.id is not None
        assert type(usuario_bd.gerar_token()) == str
        assert res.mimetype == mimetype
        assert res.status_code == 200
        assert res.json[0]['id'] != None


def test_usuario_logout(app, client):
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(admin=True).first()

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': f'JWT {usuario_bd.gerar_token()}'
        }

        url = '/api-flask-exemplo/v1/usuario/logout'

        res = client.delete(url, headers=headers)
        assert res.mimetype == mimetype
        assert res.status_code == 204

        # Verificar se fez o logout
        url = '/api-flask-exemplo/v1/usuario/token/check'
        res = client.get(url, headers=headers)
        assert res.mimetype == mimetype
        assert res.status_code == 401
        

def test_usuario_obter_dados_token(app, client):
    with app.app_context():
        from app.models.usuario import Usuario
        usuario_bd = Usuario.query.filter_by(email='obedera@gmail.com').first()

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': f'JWT {usuario_bd.gerar_token()}'
        }

        url = '/api-flask-exemplo/v1/usuario/token/dados'

        res = client.get(url, headers=headers)
        assert res.mimetype == mimetype
        assert res.status_code == 200
        assert res.json['nome'] == 'Obedera'
        assert res.json['email'] == 'obedera@gmail.com'
