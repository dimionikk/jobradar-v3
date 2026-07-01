import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import asyncsessionLocal
from app.parsers.remotive import parse_remotive
from app.parsers.dou import parse_dou
from app.parsers.djinni import parse_djinni
from app.parsers.workua import parse_workua
from app.services.parser import save_vacancies

scheduler = AsyncIOScheduler()


async def run_parsers_job():
    print("Запуск парсерів...")

    all_vacancies = []

    try:
        all_vacancies += await parse_remotive()
    except Exception as e:
        print(f"Помилка парсингу Remotive: {e}")

    try:
        all_vacancies += await asyncio.to_thread(parse_dou)
    except Exception as e:
        print(f"Помилка парсингу DOU: {e}")

    try:
        all_vacancies += await asyncio.to_thread(parse_djinni)
    except Exception as e:
        print(f"Помилка парсингу Djinni: {e}")

    try:
        all_vacancies += await asyncio.to_thread(parse_workua)
    except Exception as e:
        print(f"Помилка парсингу Work.ua: {e}")

    async with asyncsessionLocal() as db:
        result = await save_vacancies(all_vacancies, db)

    print(
        f"Парсинг завершено: нових {result['new']}, "
        f"пропущено {result['skipped']}, некоректних {result['invalid']}"
    )


scheduler.add_job(run_parsers_job, "interval", hours=6)