import httpx
from bs4 import BeautifulSoup


def _strip_html(html: str | None) -> str | None:
    if not html:
        return None
    text = BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)
    return text or None


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
        title = job.get("title")
        vacancy_url = job.get("url")
        if not title or not vacancy_url:
            continue

        vacancy = {
            "title": title,
            "company": job.get("company_name"),
            "city": job.get("candidate_required_location"),
            "salary": job.get("salary") or None,
            "work_type": job.get("job_type"),
            "description": _strip_html(job.get("description")),
            "url": vacancy_url,
            "source": "remotive",
        }
        vacancies.append(vacancy)

    return vacancies