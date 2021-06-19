from datetime import datetime, timedelta

def test_model_usuario(app, client):
    from app.models.usuario import Usuario

    usuario_bd = Usuario(
        id=1,
        nome='Obede',
        email='obede.test@gmail.com',
        senha='pokemon123',
        admin=False,
        status=False,
        data_criacao=datetime.now().replace(microsecond=0),
        data_atualizacao=datetime.now().replace(microsecond=0)
    )

    
    assert usuario_bd.nome == 'Obede'
    assert usuario_bd.email == 'obede.test@gmail.com'
    assert usuario_bd.senha == 'pokemon123'
    assert usuario_bd.admin == False
    assert usuario_bd.status == False
    assert usuario_bd.data_criacao != None
    assert usuario_bd.data_atualizacao != None
    assert usuario_bd.id is not None
    assert type(usuario_bd.gerar_token()) == str
    