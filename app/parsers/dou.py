import httpx
from bs4 import BeautifulSoup


def parse_dou() -> list[dict]:
    url = "https://jobs.dou.ua/vacancies/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = httpx.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    vacancies = []

    for li in soup.find_all("li", class_="l-vacancy"):
        title_tag = li.find("a", class_="vt")
        company_tag = li.find("a", class_="company")
        salary_tag = li.find("span", class_="salary")
        city_tag = li.find("span", class_="cities")
        description_tag = li.find("div", class_="sh-info")

        vacancy = {
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "url": title_tag.get("href") if title_tag else None,
            "company": company_tag.get_text(strip=True) if company_tag else None,
            "salary": salary_tag.get_text(strip=True) if salary_tag else None,
            "city": city_tag.get_text(strip=True) if city_tag else None,
            "description": description_tag.get_text(strip=True) if description_tag else None,
            "work_type": None,
            "source": "dou",
        }
        vacancies.append(vacancy)

    return vacancies