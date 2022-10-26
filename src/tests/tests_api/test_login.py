from starlette.testclient import TestClient

URL = '/api/v1/auth/login'


def test_login_existing_user(test_client: TestClient, create_user_db):
    body = {
        'username': 'Test1',
        'password': 'password'
    }
    response = test_client.post(URL, json=body)
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_login_not_existing_user(test_client: TestClient, create_user_db):
    body = {
        'username': 'Test2',
        'password': 'password'
    }
    response = test_client.post(URL, json=body)
    assert response.status_code == 404
    assert 'Пользователь не найден' in response.json()['detail']


def test_login_wrong_password(test_client: TestClient, create_user_db):
    body = {
        'username': 'Test1',
        'password': 'passwordWrong'
    }
    response = test_client.post(URL, json=body)
    assert response.status_code == 400
    assert 'Неверный пароль' in response.json()['detail']