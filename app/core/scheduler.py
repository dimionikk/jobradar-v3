import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.database import AsyncSessionLocal
from app.parsers.remotive import parse_remotive
from app.parsers.dou import parse_dou
from app.parsers.djinni import parse_djinni
from app.parsers.workua import parse_workua
from app.services.parser import save_vacancies

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_parsers_job():
    logger.info("Запуск парсерів...")
    all_vacancies = []

    try:
        all_vacancies += await parse_remotive()
    except Exception:
        logger.exception("Помилка парсингу Remotive")

    try:
        all_vacancies += await asyncio.to_thread(parse_dou)
    except Exception:
        logger.exception("Помилка парсингу DOU")

    try:
        all_vacancies += await asyncio.to_thread(parse_djinni)
    except Exception:
        logger.exception("Помилка парсингу Djinni")

    try:
        all_vacancies += await asyncio.to_thread(parse_workua)
    except Exception:
        logger.exception("Помилка парсингу Work.ua")

    try:
        async with AsyncSessionLocal() as db:
            result = await save_vacancies(all_vacancies, db)
    except Exception:
        logger.exception("Помилка збереження вакансій у базу")
        return

    logger.info(
        "Парсинг завершено: нових %s, пропущено %s, некоректних %s",
        result["new"], result["skipped"], result["invalid"],
    )


scheduler.add_job(run_parsers_job, "interval", hours=6)