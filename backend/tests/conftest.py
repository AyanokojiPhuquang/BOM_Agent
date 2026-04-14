import httpx
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8030"


@pytest.fixture(scope="session")
def client(base_url):
    with httpx.Client(base_url=base_url, timeout=30.0) as c:
        yield c


@pytest.fixture(scope="session")
def auth_token(client):
    resp = client.post(
        "/api/auth/login",
        json={"email": "demo@starlink.chat", "password": "password"},
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
