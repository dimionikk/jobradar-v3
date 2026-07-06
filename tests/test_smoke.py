async def test_register_and_login(client):
    register_response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert register_response.status_code == 200

    login_response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
