async def test_save_vacancy(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    response = await client.post(f"/saved-vacancies/{ids[0]}", headers=auth_headers)
    assert response.status_code == 201


async def test_save_nonexistent_vacancy(client, auth_headers):
    response = await client.post("/saved-vacancies/9999", headers=auth_headers)
    assert response.status_code == 404


async def test_save_duplicate_vacancy(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    await client.post(f"/saved-vacancies/{ids[0]}", headers=auth_headers)
    response = await client.post(f"/saved-vacancies/{ids[0]}", headers=auth_headers)
    assert response.status_code == 400


async def test_get_saved_vacancies(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=3)
    for vacancy_id in ids:
        await client.post(f"/saved-vacancies/{vacancy_id}", headers=auth_headers)

    response = await client.get("/saved-vacancies/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_remove_saved_vacancy(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    await client.post(f"/saved-vacancies/{ids[0]}", headers=auth_headers)

    response = await client.delete(f"/saved-vacancies/{ids[0]}", headers=auth_headers)
    assert response.status_code == 200

    get_response = await client.get("/saved-vacancies/", headers=auth_headers)
    assert get_response.json() == []


async def test_remove_nonexistent_saved_vacancy(client, auth_headers, seed_vacancies):
    ids = await seed_vacancies(count=1)
    response = await client.delete(f"/saved-vacancies/{ids[0]}", headers=auth_headers)
    assert response.status_code == 404


async def test_saved_vacancies_isolated_between_users(client, seed_vacancies):
    ids = await seed_vacancies(count=1)

    await client.post("/auth/register", json={"email": "user1@example.com", "password": "testpassword123"})
    login1 = await client.post("/auth/login", json={"email": "user1@example.com", "password": "testpassword123"})
    headers1 = {"Authorization": f"Bearer {login1.json()['access_token']}"}

    await client.post("/auth/register", json={"email": "user2@example.com", "password": "testpassword123"})
    login2 = await client.post("/auth/login", json={"email": "user2@example.com", "password": "testpassword123"})
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    await client.post(f"/saved-vacancies/{ids[0]}", headers=headers1)

    response2 = await client.get("/saved-vacancies/", headers=headers2)
    assert response2.json() == []

    response1 = await client.get("/saved-vacancies/", headers=headers1)
    assert len(response1.json()) == 1
