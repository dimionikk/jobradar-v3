import logging

import httpx
from bs4 import BeautifulSoup

from app.parsers.utils import DEFAULT_HEADERS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10

WORK_TYPE_KEYWORDS = {
    "віддалено": "remote",
    "remote": "remote",
    "гібрид": "hybrid",
    "hybrid": "hybrid",
}


def _extract_city_and_work_type(city_tag) -> tuple[str | None, str | None]:
    if city_tag is None:
        return None, None

    raw_text = city_tag.get_text(strip=True)
    if not raw_text:
        return None, None

    parts = [p.strip() for p in raw_text.split(",")]
    work_type = None
    city_parts = []

    for part in parts:
        matched = WORK_TYPE_KEYWORDS.get(part.lower())
        if matched:
            work_type = matched
        else:
            city_parts.append(part)

    city = ", ".join(city_parts) if city_parts else None
    return city, work_type


def parse_dou() -> list[dict]:
    url = "https://jobs.dou.ua/vacancies/"
    response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("li", class_="l-vacancy")

    if not items:
        logger.warning("DOU parser found 0 vacancy items — possible HTML structure change")
        return []

    vacancies = []
    for li in items:
        title_tag = li.find("a", class_="vt")
        if title_tag is None:
            continue

        title = title_tag.get_text(strip=True)
        vacancy_url = title_tag.get("href")
        if not title or not vacancy_url:
            continue

        company_tag = li.find("a", class_="company")
        salary_tag = li.find("span", class_="salary")
        city_tag = li.find("span", class_="cities")
        description_tag = li.find("div", class_="sh-info")

        city, work_type = _extract_city_and_work_type(city_tag)

        vacancy = {
            "title": title,
            "url": vacancy_url,
            "company": company_tag.get_text(strip=True) if company_tag else None,
            "salary": salary_tag.get_text(strip=True) if salary_tag else None,
            "city": city,
            "description": description_tag.get_text(strip=True) if description_tag else None,
            "work_type": work_type,
            "source": "dou",
        }
        vacancies.append(vacancy)

    return vacancies