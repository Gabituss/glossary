from typing import Optional, List
from loguru import logger

from bot.models import Template
from random import randint


async def create_template(**kwargs) -> Optional[Template]:
    template = await Template.create(template_id=await get_id(), **kwargs)
    logger.info(f"New template: {template}")
    return template


async def delete_template(template_id: int) -> None:
    logger.info(f"Template deleted: {template_id}")
    await Template.filter(template_id=template_id).delete()


async def get(template_id: int) -> Optional[Template]:
    if not await template_exists(template_id):
        logger.error(f"Template {template_id} does not exists")
        raise ValueError
    return await Template.get(template_id=template_id)


async def get_all() -> List[Template]:
    return await Template.all()


async def get_id() -> int:
    return randint(0, 10 ** 9)


async def template_exists(template_id: int) -> bool:
    if await Template.filter(template_id=template_id).first():
        return True
    return False
