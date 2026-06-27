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

    remotive_data = await parse_remotive()
    dou_data = await asyncio.to_thread(parse_dou)
    djinni_data = await asyncio.to_thread(parse_djinni)
    workua_data = await asyncio.to_thread(parse_workua)

    all_vacancies = remotive_data + dou_data + djinni_data + workua_data

    async with asyncsessionLocal() as db:
        result = await save_vacancies(all_vacancies, db)

    print(f"Парсинг завершено: нових {result['new']}, пропущено {result['skipped']}")


scheduler.add_job(run_parsers_job, "interval", seconds=10)