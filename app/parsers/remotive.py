import httpx

url = "https://remotive.com/api/remote-jobs?category=software-dev"


async def parse_remotive() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    vacancies = []
    for job in data["jobs"]:
        vacancy = {
            "title": job["title"],
            "company": job["company_name"],
            "city": job["candidate_required_location"],
            "salary": job["salary"],
            "work_type": job["job_type"],
            "description": job["description"],
            "url": job["url"],
            "source": "remotive",
        }
        vacancies.append(vacancy)

    return vacancies