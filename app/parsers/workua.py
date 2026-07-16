import logging
import re

import httpx
from bs4 import BeautifulSoup

from app.parsers.utils import DEFAULT_HEADERS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10

# Підтверджено на одному зразку: опис часто починається з "Тип зайнятості. Досвід роботи ... ."
# перед реальним текстом. Якщо на ширшій вибірці патерн не спрацює — description
# просто лишиться нерозбитим (fallback у кінці функції).
_META_PREFIX_RE = re.compile(r"^([^.]+\.)\s*([^.]*досвід[^.]*\.)?\s*(.*)$", re.IGNORECASE | re.DOTALL)


def _split_description_meta(text: str | None) -> tuple[str | None, str | None, str | None]:
    if not text:
        return None, None, None
    match = _META_PREFIX_RE.match(text)
    if not match:
        return None, None, text
    work_type = match.group(1).strip().rstrip(".") or None
    experience = match.group(2).strip().rstrip(".") if match.group(2) else None
    description = match.group(3).strip() or None
    return work_type, experience, description


def parse_workua() -> list[dict]:
    url = "https://www.work.ua/jobs-it/"
    response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="job-link")

    if not cards:
        logger.warning("Work.ua parser found 0 vacancy cards — possible HTML structure change")
        return []

    vacancies = []
    for card in cards:
        title_tag = card.find("h2", class_="my-0")
        link_tag = title_tag.find("a") if title_tag else None
        title = link_tag.get_text(strip=True) if link_tag else None
        href = link_tag.get("href") if link_tag else None
        job_url = f"https://www.work.ua{href}" if href else None

        if not title or not job_url:
            continue

        strong_spans = card.find_all("span", class_="strong-600")
        if len(strong_spans) >= 2:
            salary = strong_spans[0].get_text(strip=True)
            company = strong_spans[1].get_text(strip=True)
        elif len(strong_spans) == 1:
            salary = None
            company = strong_spans[0].get_text(strip=True)
        else:
            salary = None
            company = None

        city_block = card.find("div", class_="text-indent")
        city = None
        if city_block:
            spans = city_block.find_all("span", recursive=False)
            for span in spans:
                classes = span.get("class") or []
                if "distance-block" in classes:
                    continue
                text = span.get_text(strip=True).strip(", ")
                if text:
                    city = text

        description_tag = card.find("p", class_="ellipsis-line-3")
        raw_description = description_tag.get_text(strip=True) if description_tag else None
        work_type, experience, description = _split_description_meta(raw_description)

        vacancy = {
            "title": title,
            "url": job_url,
            "salary": salary,
            "company": company,
            "city": city,
            "description": description,
            "work_type": work_type,
            "experience": experience,
            "source": "workua",
        }
        vacancies.append(vacancy)

    return vacancies