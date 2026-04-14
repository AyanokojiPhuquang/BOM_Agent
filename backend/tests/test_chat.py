def test_chat_completion_non_streaming(client, auth_headers):
    resp = client.post(
        "/api/chat/completions",
        headers=auth_headers,
        json={
            "model": "anthropic/claude-haiku-4.5",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False,
        },
        timeout=60.0,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert "choices" in data
    assert isinstance(data["choices"], list)
    assert len(data["choices"]) > 0
    choice = data["choices"][0]
    assert choice["message"]["role"] == "assistant"
    assert isinstance(choice["message"]["content"], str)
    assert len(choice["message"]["content"]) > 0

    # cleanup auto-created conversation
    conv_id = data.get("conversation_id")
    if conv_id:
        client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)
