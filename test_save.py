import asyncio
from app.core.database import asyncsessionLocal
from app.parsers.remotive import parse_remotive
from app.parsers.dou import parse_dou
from app.parsers.djinni import parse_djinni
from app.parsers.workua import parse_workua
from app.services.parser import save_vacancies


async def main():
    remotive = await parse_remotive()
    dou = parse_dou()
    djinni = parse_djinni()
    workua = parse_workua()

    all_vacancies = remotive + dou + djinni + workua
    print(f"Зібрано з парсерів: {len(all_vacancies)}")

    async with asyncsessionLocal() as db:
        result = await save_vacancies(all_vacancies, db)
        print(f"Нових: {result['new']}")
        print(f"Пропущено (вже були): {result['skipped']}")


asyncio.run(main())
