import httpx


async def parse_remotive() -> list[dict]:
    url = "https://remotive.com/api/remote-jobs?category=software-dev"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            return []

    jobs = data.get("jobs")
    if not jobs:
        return []

    vacancies = []
    for job in jobs:
        vacancy = {
            "title": job.get("title"),
            "company": job.get("company_name"),
            "city": job.get("candidate_required_location"),
            "salary": job.get("salary"),
            "work_type": job.get("job_type"),
            "description": job.get("description"),
            "url": job.get("url"),
            "source": "remotive",
        }
        vacancies.append(vacancy)

    return vacancies