async def test_get_vacancies_empty(client, auth_headers):
    response = await client.get("/vacancies/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_vacancies_list(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=3)
    response = await client.get("/vacancies/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_vacancies_without_token(client):
    response = await client.get("/vacancies/")
    assert response.status_code == 401


async def test_search_filter(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=1, title="Java Backend Engineer")
    await seed_vacancies(count=1, title="Python Backend Engineer")

    response = await client.get("/vacancies/?search=Python", headers=auth_headers)
    data = response.json()
    assert len(data) == 1
    assert "Python" in data[0]["title"]


async def test_city_filter(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=1, city="Lviv")
    await seed_vacancies(count=1, city="Kyiv")

    response = await client.get("/vacancies/?city=Lviv", headers=auth_headers)
    data = response.json()
    assert len(data) == 1
    assert data[0]["city"] == "Lviv"


async def test_source_filter(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=1, source="dou")
    await seed_vacancies(count=1, source="djinni")

    response = await client.get("/vacancies/?source=dou", headers=auth_headers)
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "dou"


async def test_pagination(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=25)

    page1 = await client.get("/vacancies/?page=1", headers=auth_headers)
    page2 = await client.get("/vacancies/?page=2", headers=auth_headers)

    assert len(page1.json()) == 20
    assert len(page2.json()) == 5


async def test_inactive_vacancy_excluded(client, auth_headers, seed_vacancies):
    await seed_vacancies(count=1, is_active=False)
    response = await client.get("/vacancies/", headers=auth_headers)
    assert response.json() == []