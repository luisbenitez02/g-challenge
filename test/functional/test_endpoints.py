def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == True

def test_hired_quarter(client):
    response = client.get('/hired_quarter')
    assert response.status_code == 200

def test_hired_department(client):
    response = client.get('/hired_department')
    assert response.status_code == 200