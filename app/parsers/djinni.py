import json
import logging

import httpx
from bs4 import BeautifulSoup

from app.parsers.utils import DEFAULT_HEADERS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10


def _extract_city(job: dict) -> str | None:
    location = job.get("jobLocation")
    if isinstance(location, list):
        location = location[0] if location else None
    if not isinstance(location, dict):
        return None
    address = location.get("address")
    if isinstance(address, dict):
        return address.get("addressLocality") or address.get("addressRegion")
    if isinstance(address, str):
        return address
    return None


def _extract_salary(job: dict) -> str | None:
    salary_info = job.get("baseSalary")
    if not salary_info:
        return None

    salary_value = salary_info.get("value", {})
    min_val = salary_value.get("minValue")
    max_val = salary_value.get("maxValue")
    currency = salary_info.get("currency") or salary_value.get("currency") or "USD"

    if min_val is not None and max_val is not None:
        return f"{min_val}-{max_val} {currency}"
    if max_val is not None:
        return f"до {max_val} {currency}"
    if min_val is not None:
        return f"від {min_val} {currency}"
    return None


def parse_djinni() -> list[dict]:
    url = "https://djinni.co/jobs/"
    response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag is None or not script_tag.string:
        return []

    try:
        jobs_data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        logger.exception("Failed to parse Djinni JSON-LD")
        return []

    if isinstance(jobs_data, dict):
        jobs_data = [jobs_data]
    if not isinstance(jobs_data, list):
        logger.error("Unexpected Djinni JSON-LD structure: %s", type(jobs_data))
        return []

    vacancies = []
    for job in jobs_data:
        if not isinstance(job, dict):
            continue

        hiring_org = job.get("hiringOrganization")
        if isinstance(hiring_org, dict):
            company = hiring_org.get("name")
        else:
            company = hiring_org

        vacancy = {
            "title": job.get("title"),
            "company": company,
            "description": job.get("description"),
            "url": job.get("url"),
            "salary": _extract_salary(job),
            "work_type": job.get("employmentType"),
            "city": _extract_city(job),
            "source": "djinni",
        }
        vacancies.append(vacancy)

    return vacancies