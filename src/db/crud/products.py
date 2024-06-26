from random import randint
from sqlalchemy import insert, select
from schemas.exceptions import BaseDBException
from schemas.products import ProductSchema
from db.models.products import Product
from utils import get_client
from db.db import new_session


async def get_relative_products(
        user_id: int) -> list[ProductSchema]:
    try:
        async with new_session.begin() as session:
            client = get_client(user_id)
            bussines_type = True if client["type"] == "ООО" else False
            stmt = select(Product).where(
                Product.is_organisation == bussines_type)
            models = [i.to_read_model() for i in (await session.scalars(stmt)).all()]
            return [models[randint(0, len(models) - 1)]]
    except Exception as e:
        raise e


async def fill_defaults():
    try:
        data = [
            {"name": "Бизнес карта для компаний", "description": "Обслуживание — 0 ₽. Привязана к расчетному счету. Для бизнес-расходов и личных трат",
                "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/eq6u9Va.png"},
            {"name": "Бизнес карта для ИП", "description": "Обслуживание — 0 ₽. Привязана к расчетному счету. Для бизнес-расходов и личных трат",
                "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/eq6u9Va.png"},
            {"name": "Онлайн банк для малого бизнеса", "description": "Без очередей и ожидания на линии. Удобное приложение и личный кабинет. Поддержка 24/7 в чате",
                "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/JKPzbv5.png"},
            {"name": "Онлайн банк для малого бизнеса", "description": "Без очередей и ожидания на линии. Удобное приложение и личный кабинет. Поддержка 24/7 в чате",
                "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/JKPzbv5.png"},
            {"name": "Кредит на развитие бизнеса", "description": "Получите деньги на развитие бизнеса: до 10 млн рублей. Вы можете узнать сумму без открытия счета.",
                "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/Gs43rcp.png"},
            {"name": "Кредит на развитие бизнеса", "description": "Получите деньги на развитие бизнеса: до 10 млн рублей. Вы можете узнать сумму без открытия счета.",
                "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/Gs43rcp.png"},
            {"name": "Бесплатная онлайн бухгалтерия для ИП", "description": "Легко сдавать отчетность и платить налоги самостоятельно.",
                "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/FpjGOHA.png"},
            {"name": "Удобный прием платежей для вашего бизнеса", "description": "Принимайте платежи от клиентов на сайте, в приложении, соцсетях, месседжерах, по e-mail и СМС",
                "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/eq6u9Va.png"},
            {"name": "Удобный прием платежей для вашего бизнеса", "description": "Принимайте платежи от клиентов на сайте, в приложении, соцсетях, месседжерах, по e-mail и СМС",
                "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://i.imgur.com/eq6u9Va.png"},
        ]
        async with new_session.begin() as session:

            existing_rows_count = await session.scalar(select(Product).limit(1))
            if not existing_rows_count:
                stmt = insert(Product).values(data)
                await session.execute(stmt)
    except:
        raise BaseDBException
