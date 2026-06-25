import re
import html
import feedparser


SALARY_PATTERN = re.compile(r"(?:від|до)?\s*\$[\d.\u2013\u2014-]+")


def parse_dou() -> list[dict]:
    url = "https://jobs.dou.ua/vacancies/feeds/"
    feed = feedparser.parse(url)

    vacancies = []
    for entry in feed.entries:
        title_raw = html.unescape(entry.title)

        try:
            job_title, rest = title_raw.split(" в ", 1)
        except ValueError:
            continue

        salary_match = SALARY_PATTERN.search(rest)
        salary = salary_match.group().strip() if salary_match else None
        if salary_match:
            rest = rest.replace(salary_match.group(), "")

        parts = [p.strip() for p in rest.split(",") if p.strip()]
        company = parts[0] if parts else None
        city = ", ".join(parts[1:]) if len(parts) > 1 else None

        vacancy = {
            "title": job_title.strip(),
            "company": company,
            "city": city,
            "salary": salary,
            "description": entry.summary,
            "url": entry.link,
            "source": "dou",
        }
        vacancies.append(vacancy)

    return vacancies