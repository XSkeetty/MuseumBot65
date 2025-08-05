from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile

from app.config import bot
from app.requests import db_requests as db
from app.utils import log_sender as logs
from app.utils.generation.generation import generation_start
from app.windows import window_constructor as windows
from app.windows.window_updater import update_window

router = Router()


@router.callback_query(F.data == 'generate')
async def generate_window(update: CallbackQuery) -> None:
    tg_user = update.from_user
    db_user = await db.get_user(tg_user)

    window = await windows.get_generation_window()
    message = await update_window(update, window)

    result = await generation_start(db_user)

    read_timer = 0
    error_counter = 0

    # while not task.done():
    #     await asyncio.sleep(1)
    #
    #     if read_timer != 3:
    #         read_timer += 1
    #         continue
    #
    #     while True:
    #         await asyncio.sleep(0.1)
    #         try:
    #             fact = random.choice(FACTS)
    #             await bot.edit_message_caption(
    #                 chat_id=tg_user.id,
    #                 message_id=message.message_id,
    #                 caption=f'{message.caption.split(':')[0]}:\n<blockquote>{fact}</blockquote>',
    #                 reply_markup=message.reply_markup
    #             )
    #             read_timer = 0
    #             break
    #         except asyncio.CancelledError:
    #             raise
    #         except Exception:
    #             if error_counter < 99:
    #                 error_counter += 1
    #             else:
    #                 break
    #
    # result = await task

    if result[0] == 'ERROR':
        if result[1] == 'GET_PHOTO':
            ex = result[2]
            for_user = 'Ошибка получения/обработки фото.\nПопробуйте снова.'
            for_logs = f'<b>Ошибка при получении/обработке фото:</b>\n<blockquote>{ex}</blockquote>'
        elif result[1] == 'RESTORE_PHOTO':
            ex = result[2]
            for_user = 'Ошибка финальной обработки фото.\nПопробуйте снова.'
            for_logs = f'<b>Ошибка при склеивании результата:</b>\n<blockquote>{ex}</blockquote>'
        elif result[1] == 'FACE_SWAP_NULL':
            for_user = 'Не смогли распознать лицо.\nПопробуйте использовать другую фотографию.'
            for_logs = f'<b>Ошибка в распозновании лица.</b>'
        elif result[1].startswith('FACE_SWAP'):
            ex = result[1].split('_')[-1]
            for_user = 'Произошла ошибка при создании изображения. Мы уже разбираемся в проблеме.\nПопробуйте снова.'
            for_logs = f'<b>Непредвиденная ошибка от модели:</b>\n<blockquote>{ex}</blockquote>'
        else:
            ex = result[1]
            for_user = 'Произошла непредвиденная ошибка. Мы уже разбираемся в проблеме.\nПопробуйте снова.'
            for_logs = f'<b>Непредвиденная ошибка при генерации:</b>\n<blockquote>{ex}</blockquote>'
    else:
        for_user = ('<b>Ваше изображение готово!</b>\n\n'
                    '<i>Мы не храним результаты ваших генераций. '
                    'Сохраните изображение вручную перед закрытием окна (если необходимо).</i>')

    if result[0] == 'SUCCESS':
        new_window = await windows.get_generation_success_window(result)
        new_message = await bot.send_photo(
            chat_id=tg_user.id,
            photo=BufferedInputFile(result[1].read(), filename='Museum65_bot.jpg'),
            caption=for_user,
            reply_markup=new_window.markup
        )
        await logs.photo_created(tg_user, db_user, new_message.photo[-1].file_id)
    else:
        new_window = await windows.get_generation_error_window()
        new_window.caption = for_user
        new_message = await update_window(update, new_window, is_new=True)
        await logs.generation_error(tg_user, db_user, for_logs)

