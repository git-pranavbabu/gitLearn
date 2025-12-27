from app import schemas
from app.config import settings
from jose import jwt
import pytest

def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"data": "Hello World"}

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@example.com", "password": "password123", "username": "hello"})
    assert res.status_code == 201
    new_user = schemas.ResponseUser(**res.json())
    assert new_user.id 
    assert new_user.created_at

def test_login_user(client, test_user):
    res = client.post("/auth/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert res.status_code == 200
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test@example.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test@example.com', None, 422)
])
def test_login_user_wrong_credentials(client, test_user, email, password, status_code):
    res = client.post("/auth/login", data={"username": email if email is not None else "", "password": password if password is not None else ""})
    assert res.status_code == status_code
