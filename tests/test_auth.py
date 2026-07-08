async def test_register_success(client):
    response = await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "hashed_password" not in data


async def test_register_duplicate_email(client):
    payload = {"email": "user@example.com", "password": "testpassword123"}
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 400


async def test_register_short_password(client):
    response = await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "short"},
    )
    assert response.status_code == 422


async def test_login_success(client):
    payload = {"email": "user@example.com", "password": "testpassword123"}
    await client.post("/auth/register", json=payload)

    response = await client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password(client):
    await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "testpassword123"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_login_nonexistent_user(client):
    response = await client.post(
        "/auth/login",
        json={"email": "ghost@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 401


async def test_logout(client):
    payload = {"email": "user@example.com", "password": "testpassword123"}
    await client.post("/auth/register", json=payload)
    login_response = await client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]

    response = await client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
