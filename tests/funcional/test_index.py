import json


def test_index(app, client):
    res = client.get('/api-flask-exemplo/')
    assert res.status_code == 200