import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.config import ACTIVATION_CODE, bot
from app.requests import db_requests as db
from app.requests.db_requests import change_user_data
from app.utils import log_sender as logs
from app.windows import window_constructor as windows
from app.windows.window_updater import update_window

router = Router()


@router.message(F.text == f'/start {ACTIVATION_CODE}')
async def auth_handler(update: Message) -> None:
    tg_user = update.from_user
    db_user = await db.get_user(tg_user)

    if not db_user.is_active:
        await db.change_user_data(tg_user, 'is_active', True)
        await logs.user_activated(tg_user)

    await start_handler(update)


@router.message(F.text == '/start')
@router.callback_query(F.data == 'start')
async def start_handler(update: Message | CallbackQuery):
    tg_user = update.from_user
    db_user = await change_user_data(tg_user, 'is_uploading_photo', False)

    if db_user.is_active:
        window = await windows.get_start_window()
    else:
        window = await windows.get_auth_window()

    message = await update_window(update, window, is_new=isinstance(update, Message))

    if isinstance(update, Message):
        last_message, user_message = db_user.last_message_id or 1, update.message_id

        try:
            await bot.delete_messages(tg_user.id, [last_message, user_message])
        except Exception as ex:
            print(ex)

        await db.change_user_data(tg_user, 'last_message_id', message.message_id)


@router.callback_query(F.data == 'about')
async def about_handler(update: CallbackQuery) -> None:
    window = await windows.get_about_window()
    await update_window(update, window)


@router.callback_query(F.data == 'album')
async def album_handler(update: CallbackQuery) -> None:
    tg_user = update.from_user
    db_user = await db.get_user(tg_user)
    window = await windows.get_album_window(db_user.template_id)
    await update_window(update, window)


@router.callback_query(F.data.startswith('template_'))
async def template_handler(update: CallbackQuery, template_id: int = None) -> None:
    template_id = template_id or update.data.split('_')[-1]
    tg_user = update.from_user
    window = await windows.get_template_window(template_id)
    await update_window(update, window)
    await db.change_user_data(tg_user, 'template_id', template_id, uploading_photo_state=False)


@router.callback_query(F.data.startswith('user_photo'))
async def user_photo_handler(update: CallbackQuery) -> None:
    tg_user = update.from_user

    if update.data.endswith('_gender'):
        db_user = await db.change_user_data(tg_user, 'gender', '', uploading_photo_state=True)
    elif update.data.endswith('_previous'):
        db_user = await db.change_user_data(tg_user, 'is_uploading_photo', False)
        window = await windows.get_confirmation_window(db_user)
        await update_window(update, window)
        return
    else:
        db_user = await db.change_user_data(tg_user, 'is_uploading_photo', True)

    window = await windows.get_user_photo_window(db_user.template_id, db_user.gender, db_user.last_photo_id)
    await update_window(update, window)


@router.message(F.photo)
async def photo_handler(update: Message) -> None:
    tg_user = update.from_user
    db_user = await db.get_user(tg_user)

    if not db_user.is_uploading_photo:
        print(f'PHOTO ID: {update.photo[-1].file_id}')

        await bot.delete_message(tg_user.id, update.message_id)
        return

    db_user = await db.change_user_data(tg_user, 'last_photo_id', update.photo[-1].file_id)

    window = await windows.get_confirmation_window(db_user)
    try: await update_window(update, window, message_id=db_user.last_message_id)
    except: pass
    await bot.delete_message(tg_user.id, update.message_id)


@router.message(F.document)
async def document_handler(update: Message) -> None:
    tg_user = update.from_user
    db_user = await db.get_user(tg_user)

    if not db_user.is_uploading_photo:
        await bot.delete_message(tg_user.id, update.message_id)
        return


    message_text = ('<b>Мы не можем использовать этот файл, так как вы отправили его документом,'
                    ' а не фотографией.\n\nАвто-удаление через:</b>')

    message = await bot.send_message(
        chat_id=tg_user.id,
        text=f'{message_text} <b>5..</b>'
    )

    for index in range(4, -2, -1):
        if index == -1:
            await bot.delete_messages(tg_user.id, [message.message_id, update.message_id])
            return

        await asyncio.sleep(1)
        await bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=message.message_id,
            text=f'{message_text} {index}..'
        )


@router.callback_query(F.data == 'close_window')
async def close_window_handler(update: CallbackQuery):
    tg_user = update.from_user
    try:
        await bot.delete_message(chat_id=tg_user.id, message_id=update.message.message_id)
        await update.answer()
    except: pass
