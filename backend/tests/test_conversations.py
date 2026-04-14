def test_create_conversation(client, auth_headers):
    resp = client.post("/api/conversations", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["id"], str) and len(data["id"]) > 0
    assert "title" in data
    assert isinstance(data["messages"], list)
    assert isinstance(data["createdAt"], int)
    assert isinstance(data["updatedAt"], int)
    # cleanup
    client.delete(f"/api/conversations/{data['id']}", headers=auth_headers)


def test_list_conversations(client, auth_headers):
    create_resp = client.post("/api/conversations", headers=auth_headers)
    conv_id = create_resp.json()["id"]

    resp = client.get("/api/conversations", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    item = data["items"][0]
    assert "id" in item
    assert "title" in item
    assert "createdAt" in item
    assert "updatedAt" in item

    client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)


def test_get_conversation(client, auth_headers):
    create_resp = client.post("/api/conversations", headers=auth_headers)
    conv_id = create_resp.json()["id"]

    resp = client.get(f"/api/conversations/{conv_id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == conv_id
    assert "title" in data
    assert isinstance(data["messages"], list)

    client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)


def test_update_conversation_title(client, auth_headers):
    create_resp = client.post("/api/conversations", headers=auth_headers)
    conv_id = create_resp.json()["id"]

    resp = client.put(
        f"/api/conversations/{conv_id}/title",
        headers=auth_headers,
        json={"title": "Smoke Test Title"},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Smoke Test Title"

    client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)


def test_delete_conversation(client, auth_headers):
    create_resp = client.post("/api/conversations", headers=auth_headers)
    conv_id = create_resp.json()["id"]

    resp = client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)
    assert resp.status_code == 204

    # verify it's gone
    get_resp = client.get(f"/api/conversations/{conv_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_get_conversation_not_found(client, auth_headers):
    resp = client.get(
        "/api/conversations/nonexistent-id-00000", headers=auth_headers
    )
    assert resp.status_code == 404
