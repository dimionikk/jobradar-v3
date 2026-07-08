async def test_create_application(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    response = await client.post(f"/applications/{ids[0]}", headers=auth_headers)
    assert response.status_code == 201


async def test_create_application_nonexistent_vacancy(client, auth_headers):
    response = await client.post("/applications/9999", headers=auth_headers)
    assert response.status_code == 404


async def test_create_duplicate_application(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    await client.post(f"/applications/{ids[0]}", headers=auth_headers)
    response = await client.post(f"/applications/{ids[0]}", headers=auth_headers)
    assert response.status_code == 400


async def test_get_applications(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=2)
    for vacancy_id in ids:
        await client.post(f"/applications/{vacancy_id}", headers=auth_headers)

    response = await client.get("/applications/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["status"] == "applied"
    assert "vacancy" in data[0]


async def test_update_application_status(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    create_response = await client.post(f"/applications/{ids[0]}", headers=auth_headers)

    apps = await client.get("/applications/", headers=auth_headers)
    application_id = apps.json()[0]["id"]

    response = await client.patch(
        f"/applications/{application_id}",
        json={"status": "interview"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "interview"


async def test_update_application_invalid_status(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    await client.post(f"/applications/{ids[0]}", headers=auth_headers)
    apps = await client.get("/applications/", headers=auth_headers)
    application_id = apps.json()[0]["id"]

    response = await client.patch(
        f"/applications/{application_id}",
        json={"status": "not_a_real_status"},
        headers=auth_headers,
    )
    assert response.status_code == 422


async def test_delete_application(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    await client.post(f"/applications/{ids[0]}", headers=auth_headers)
    apps = await client.get("/applications/", headers=auth_headers)
    application_id = apps.json()[0]["id"]

    response = await client.delete(f"/applications/{application_id}", headers=auth_headers)
    assert response.status_code == 200

    get_response = await client.get("/applications/", headers=auth_headers)
    assert get_response.json() == []


async def test_cannot_update_other_users_application(client, seed_vacancies):
    ids = await seed_vacancies(count=1)

    await client.post("/auth/register", json={"email": "user1@example.com", "password": "testpassword123"})
    login1 = await client.post("/auth/login", json={"email": "user1@example.com", "password": "testpassword123"})
    headers1 = {"Authorization": f"Bearer {login1.json()['access_token']}"}

    await client.post("/auth/register", json={"email": "user2@example.com", "password": "testpassword123"})
    login2 = await client.post("/auth/login", json={"email": "user2@example.com", "password": "testpassword123"})
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    await client.post(f"/applications/{ids[0]}", headers=headers1)
    apps = await client.get("/applications/", headers=headers1)
    application_id = apps.json()[0]["id"]

    response = await client.patch(
        f"/applications/{application_id}",
        json={"status": "offer"},
        headers=headers2,
    )
    assert response.status_code == 404
