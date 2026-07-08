async def test_get_profile(client, auth_headers):
    response = await client.get("/profile/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["stack"] is None


async def test_get_profile_without_token(client):
    response = await client.get("/profile/")
    assert response.status_code == 401


async def test_update_profile(client, auth_headers):
    response = await client.patch(
        "/profile/",
        json={"stack": "Python, FastAPI", "experience_years": 2, "city": "Suмy"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stack"] == "Python, FastAPI"
    assert data["experience_years"] == 2


async def test_update_profile_partial(client, auth_headers):
    await client.patch(
        "/profile/",
        json={"stack": "Python", "city": "Kyiv"},
        headers=auth_headers,
    )
    response = await client.patch(
        "/profile/",
        json={"city": "Lviv"},
        headers=auth_headers,
    )
    data = response.json()
    assert data["city"] == "Lviv"
    assert data["stack"] == "Python"


async def test_update_profile_invalid_experience(client, auth_headers):
    response = await client.patch(
        "/profile/",
        json={"experience_years": -5},
        headers=auth_headers,
    )
    assert response.status_code == 422


async def test_delete_profile(client, auth_headers):
    response = await client.delete("/profile/", headers=auth_headers)
    assert response.status_code == 200

    get_response = await client.get("/profile/", headers=auth_headers)
    assert get_response.status_code == 401

