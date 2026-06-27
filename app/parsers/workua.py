import httpx
from bs4 import BeautifulSoup


def parse_workua() -> list[dict]:
    url = "https://www.work.ua/jobs-it/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = httpx.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    vacancies = []
    for card in soup.find_all("div", class_="job-link"):

        title_tag = card.find("h2", class_="my-0")
        link_tag = title_tag.find("a") if title_tag else None
        title = link_tag.get_text(strip=True) if link_tag else None
        job_url = "https://www.work.ua" + link_tag["href"] if link_tag else None

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

        mt_xs = card.find("div", class_="mt-xs")
        city = None
        if mt_xs:
            spans = mt_xs.find_all("span", recursive=False)
            for span in spans:
                classes = span.get("class") or []
                if "distance-block" in classes:
                    continue
                text = span.get_text(strip=True).strip(", ")
                if text:
                    city = text

        description_tag = card.find("p", class_="ellipsis-line-3")
        description = description_tag.get_text(strip=True) if description_tag else None

        vacancy = {
            "title": title,
            "url": job_url,
            "salary": salary,
            "company": company,
            "city": city,
            "description": description,
            "source": "workua",
        }
        vacancies.append(vacancy)

    return vacancies