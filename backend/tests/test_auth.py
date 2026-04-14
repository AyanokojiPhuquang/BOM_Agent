def test_login_success(client):
    resp = client.post(
        "/api/auth/login",
        json={"email": "demo@starlink.chat", "password": "password"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["token"], str) and len(data["token"]) > 0
    user = data["user"]
    assert "id" in user
    assert user["email"] == "demo@starlink.chat"
    assert "name" in user


def test_login_invalid_credentials(client):
    resp = client.post(
        "/api/auth/login",
        json={"email": "demo@starlink.chat", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_get_me(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "demo@starlink.chat"
    assert "id" in data
    assert "name" in data


def test_get_me_unauthorized(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code in (401, 403)
