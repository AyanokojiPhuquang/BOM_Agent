def test_nhanh_token_status(client):
    resp = client.get("/api/nhanh/token/status")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["connected"], bool)
    assert isinstance(data["message"], str)
