from typing import Literal, Optional

from aiogram.types import User as TG_User
from sqlalchemy import select

from app.models.database import AsyncSession, User as DB_User


ArgName = Literal[
    'is_uploading_photo',
    'generation_count',
    'last_message_id',
    'last_photo_id',
    'template_id',
    'is_active',
    'gender'
]


async def add_user(tg_user: TG_User, session: AsyncSession) -> DB_User:
    user: DB_User = DB_User(
        telegram_id=tg_user.id
    )
    session.add(user)
    await session.commit()
    return user


async def get_user(tg_user: TG_User, session: Optional[AsyncSession] = None) -> DB_User:
    async def _query(_session: AsyncSession) -> DB_User:
        stmt = select(DB_User).where(DB_User.telegram_id == tg_user.id)
        result = await _session.execute(stmt)
        user: DB_User = result.scalar_one_or_none()

        if not user:
            user = await add_user(tg_user, _session)

        return user

    if session is None:
        async with AsyncSession() as session:
            return await _query(session)
    else:
        return await _query(session)


async def change_user_data(tg_user: TG_User, arg: ArgName, value: str | int | bool,
                           uploading_photo_state: Optional[bool] = None) -> DB_User:
    async with AsyncSession() as session:
        user = await get_user(tg_user, session)

        if uploading_photo_state is not None:
            user.is_uploading_photo = uploading_photo_state

        if arg == 'gender':
            user.gender = {'male': 'female', 'female': 'male'}[user.gender]
        else:
            setattr(user, arg, value)

        await session.commit()

    return user