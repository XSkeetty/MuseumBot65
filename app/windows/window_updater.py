from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, BufferedInputFile

from app.assets.preview_file_ids import PREVIEW_IDS
from app.config import bot
from app.models.window import Window
from app.assets.image_file_ids import IMAGE_IDS


async def update_window(update: Message | CallbackQuery, window: Window, is_new: bool = False, message_id: int = None):
    split_photo_id = window.photo_id.split('/')
    photo_source = split_photo_id[0]

    if photo_source == 'images': photo = IMAGE_IDS[split_photo_id[1]]
    elif photo_source == 'previews': photo = PREVIEW_IDS[split_photo_id[1]]
    else: photo = photo_source

    if is_new:
        message = await bot.send_photo(
            chat_id=update.from_user.id,
            photo=photo,
            caption=window.caption,
            reply_markup=window.markup
        )
    else:
        message_id = message_id or update.message.message_id
        message = await bot.edit_message_media(
            chat_id=update.from_user.id,
            message_id=message_id,
            media=InputMediaPhoto(
                media=photo,
                caption=window.caption
            ),
            reply_markup=window.markup
        )

    if isinstance(update, CallbackQuery):
        try:
            await update.answer()
        except:
            pass

    return message