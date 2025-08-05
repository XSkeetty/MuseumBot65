from datetime import datetime

from aiogram.types import User as TG_User, InputMediaPhoto

from app.config import bot, CHANEL_ID
from app.models.database import User as DB_User


async def user_activated(tg_user: TG_User) -> None:
    date_now = datetime.now()
    date_formatted_1 = f'{date_now.day}{date_now.month}{date_now.strftime('%y')}'
    date_formatted_2 = date_now.strftime('%d.%m.%Y | %H:%M')
    message_text = (
        f'<b>--- Активация пользователя ---</b>\n\n'
        f'Пользователь: @{tg_user.username}\n'
        f'Имя: <code>{tg_user.full_name}</code>\n\n'
        f'<b>-- Фильтрация --</b>\n'
        f'По пользователю: #U{tg_user.id}\n'
        f'По событию: #ACTIVATION\n'
        f'По дате: #D{date_formatted_1}\n\n'
        f'Дата события:\n'
        f'<code>{date_formatted_2}</code>\n\n'
    )

    await bot.send_message(
        chat_id=CHANEL_ID,
        text=message_text
    )


async def photo_created(tg_user: TG_User, db_user: DB_User, result_photo) -> None:
    date_now = datetime.now()
    date_formatted_1 = f'{date_now.day}{date_now.month}{date_now.strftime('%y')}'
    date_formatted_2 = date_now.strftime('%d.%m.%Y | %H:%M')
    gender = {'male': 'Мужчина', 'female': 'Женщина'}
    message_text = (
        f'<b>--- Создание изображения ---</b>\n\n'
        f'Пользователь: @{tg_user.username}\n'
        f'Имя: <code>{tg_user.full_name}</code>\n'
        f'Шаблон: <code>№{db_user.template_id}</code>\n'
        f'Пол: <code>{gender[db_user.gender]}</code>\n\n'
        f'<b>-- Фильтрация --</b>\n'
        f'По пользователю: #U{tg_user.id}\n'
        f'По событию: #GENERATION\n'
        f'По шаблону: #TMP0{db_user.template_id}\n'
        f'По дате: #D{date_formatted_1}\n\n'
        f'Дата события:\n'
        f'<code>{date_formatted_2}</code>\n\n'
    )

    await bot.send_media_group(
        chat_id=CHANEL_ID,
        media=[
            InputMediaPhoto(media=result_photo, caption=message_text),
            InputMediaPhoto(media=db_user.last_photo_id, has_spoiler=True)
        ]
    )


async def generation_error(tg_user: TG_User, db_user: DB_User, error_text: str) -> None:
    date_now = datetime.now()
    date_formatted_1 = f'{date_now.day}{date_now.month}{date_now.strftime('%y')}'
    date_formatted_2 = date_now.strftime('%d.%m.%Y | %H:%M')
    message_text = (
        f'<b>--- Ошибка генерации ---</b>\n\n'
        f'Пользователь: @{tg_user.username}\n'
        f'Имя: <code>{tg_user.full_name}</code>\n\n'
        f'<b>-- Фильтрация --</b>\n'
        f'По пользователю: #U{tg_user.id}\n'
        f'По событию: #GENERROR\n'
        f'По дате: #D{date_formatted_1}\n\n'
        f'Дата события:\n'
        f'<code>{date_formatted_2}</code>\n\n'
        f'{error_text}'
    )

    await bot.send_photo(
        chat_id=CHANEL_ID,
        photo=db_user.last_photo_id,
        caption=message_text
    )