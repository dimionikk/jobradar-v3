import httpx
import json
from bs4 import BeautifulSoup
from app.parsers.utils import DEFAULT_HEADERS


def parse_djinni() -> list[dict]:
    url = "https://djinni.co/jobs/"

    response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")

    if script_tag is None:
        return []

    try:
        jobs_data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        return []

    vacancies = []
    for job in jobs_data:
        hiring_org = job.get("hiringOrganization")
        if isinstance(hiring_org, dict):
            company = hiring_org.get("name")
        else:
            company = hiring_org

        salary_info = job.get("baseSalary")
        if salary_info:
            salary_value = salary_info.get("value", {})
            min_val = salary_value.get("minValue")
            max_val = salary_value.get("maxValue")
            if min_val and max_val:
                salary = f"${min_val}-${max_val}"
            elif max_val:
                salary = f"до ${max_val}"
            elif min_val:
                salary = f"від ${min_val}"
            else:
                salary = None
        else:
            salary = None

        vacancy = {
            "title": job.get("title"),
            "company": company,
            "description": job.get("description"),
            "url": job.get("url"),
            "salary": salary,
            "work_type": job.get("employmentType"),
            "city": None,
            "source": "djinni",
        }
        vacancies.append(vacancy)

    return vacancies