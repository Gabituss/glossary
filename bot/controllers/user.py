from typing import Optional
from loguru import logger
from bot.models import User


async def create_user(user_id: int, full_name: str, username: str = None) -> Optional[User]:
    user = None
    if not await user_exists(user_id):
        user = await User.create(
            user_id=user_id,
            username=username,
            full_name=full_name,
        )
        logger.info(f"New user: {user}")

    return user


async def get(user_id: int) -> Optional[User]:
    if not await user_exists(user_id):
        logger.error(f"User {user_id} does not exists")
        raise ValueError
    return await User.get(user_id=user_id)


async def user_exists(user_id: int) -> bool:
    if await User.filter(user_id=user_id).first():
        return True
    return False
