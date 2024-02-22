from random import randint

from typing import Optional, List
from loguru import logger

from bot.models import Field


async def create_field(**kwargs) -> Optional[Field]:
    field = await Field.create(field_id=await get_id(), **kwargs)
    logger.info(f"New field: {field}")

    return field


async def update_field(field_id: int, **kwargs):
    logger.info(f"Update field: {field_id}")
    await Field.filter(field_id=field_id).update(**kwargs)


async def delete_field(field_id: int) -> None:
    logger.info(f"Field deleted: {field_id}")
    await Field.filter(field_id=field_id).delete()


async def get(field_id: int) -> Optional[Field]:
    if not await field_exists(field_id):
        logger.error(f"Field {field_id} does not exists")
        raise ValueError
    return await Field.get(field_id=field_id)


async def get_all() -> List[Field]:
    return await Field.all()


async def get_id() -> int:
    return randint(0, 10 ** 9)


async def field_exists(field_id: int) -> bool:
    if await Field.filter(field_id=field_id).first():
        return True
    return False
