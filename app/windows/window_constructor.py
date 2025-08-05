from io import BytesIO

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.assets.preview_info import INFO
from app.models.database import User as DB_User
from app.models.window import Window


async def get_auth_window() -> Window:
    photo_id = 'images/auth'
    caption = 'Данный бот доступен только для посетителей музея <b>«Россия - Моя история»</b>.'

    return Window(photo_id=photo_id, caption=caption, markup=None)


async def get_start_window() -> Window:
    photo_id = 'images/start'
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🌟 Начать', callback_data='album')],
            [InlineKeyboardButton(text='ℹ️ О проекте', callback_data='about')]
        ]
    )
    return Window(photo_id=photo_id, caption=None, markup=markup)


async def get_about_window() -> Window:
    photo_id = 'images/about'
    caption = (
        'Выставочный проект посвящён заключительному этапу Второй мировой войны и рассказывает о героических действиях '
        'советских войск на Дальнем Востоке в августе–сентябре 1945 года.\n\n'
        'Экспозиция приурочена к 80-летию Победы в Великой Отечественной войне и 130-летию со дня рождения маршала '
        'Советского Союза Александра Михайловича Василевского — одного из главных стратегов победоносной Маньчжурской '
        'операции. Проект раскрывает ход этой масштабной наступательной кампании, охватившей фронт длиной более пяти '
        'тысяч километров.\n\n'
        'Посетителей ждёт насыщенная экспозиция: редкие архивные фотографии, подлинные документы, военные карты, '
        'схемы боевых действий и агитационные плакаты. Эти материалы позволяют проследить стремительное развитие '
        'операции, её стратегические решения и решающий вклад советской армии в окончание Второй мировой войны.'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='↩️ Назад', callback_data='start')]
        ]
    )

    return Window(photo_id=photo_id, caption=caption, markup=markup)


async def get_album_window(template_id: int) -> Window:
    photo_id = 'images/album'
    caption = (
        'Мы подготовили для Вас <b>альбом</b> с историческими фотографиями.\n\n'
        '<b>Нажмите на номер</b> архивного фото чтобы ознакомиться с ним подробнее.'
    )

    builder = InlineKeyboardBuilder()

    for index in range(1, 12):
        template_status = ' • ' if index == template_id else ''
        builder.button(text=f'{template_status}№ {index}{template_status}', callback_data=f'template_{index}')

    builder.adjust(3)
    builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data='start'))
    markup = builder.as_markup()

    return Window(photo_id=photo_id, caption=caption,  markup=markup)


async def get_template_window(template_id: int):
    photo_id = f'previews/template_{template_id}'
    caption = INFO.get(f'template_{template_id}')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🎞 Стать частью фото', callback_data='user_photo')],
            [InlineKeyboardButton(text='↩️ Назад', callback_data='album')]
        ]
    )

    return Window(photo_id=photo_id, caption=caption, markup=markup)


async def get_user_photo_window(template_id: int, gender: str, last_photo_id: str):
    gender_emoji = {'male': '🧔🏻‍♂️', 'female': '👱🏼‍♀️'}
    photo_id = f'previews/template_{template_id}'
    caption = (
        'Отправьте своё фото, чтобы мы могли поместить вас в историю.\n\n'
        '<b>Требования к фото:</b>\n'
        '- Только <b>один человек</b> на фото;\n'
        '- Лицо <b>отчётливо видно</b>, вы должны смотреть в камеру;\n'
        '- Лицо <b>полностью</b> в кадре;\n'
        '- Отправляйте <b>как фото</b>, а не как документ.\n\n'
        'Результат получится лучше, если ничего не будет закрывать ваше лицо (очки, маска, шарф и т.д.).'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Выберите пол: {gender_emoji[gender]}',callback_data='user_photo_gender')],
            [InlineKeyboardButton(text='↩️ Назад', callback_data=f'template_{template_id}')]
        ]
    )

    if last_photo_id:
        new_button = [InlineKeyboardButton(text='🖼 Использовать предыдущее',callback_data='user_photo_previous')]
        markup.inline_keyboard.insert(1, new_button)

    return Window(photo_id=photo_id, caption=caption, markup=markup)


async def get_confirmation_window(db_user: DB_User) -> Window:
    gender = {'male': 'Мужчина', 'female': 'Женщина'}
    caption = (
        'Убедитесь, что всё верно и что Ваше фото соответствует требованиям, после чего можете начать создание.'
        f'\n\n<b>Архивное фото: </b><code>№{db_user.template_id}</code>\n'
        f'<b>Пол:</b> <code>{gender[db_user.gender]}</code>\n\n'
        f'<i>* Вы можете изменить фото на этом шаге, просто отправив его в чат.</i>')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'🪄 Создать', callback_data='generate')],
            [InlineKeyboardButton(text='🚫 Отмена', callback_data=f'user_photo')]
        ]
    )

    return Window(photo_id=db_user.last_photo_id, caption=caption, markup=markup)


async def get_generation_window() -> Window:
    photo_id = 'images/generation'
    caption = ('Мы уже создаём ваше изображение.\n\n'
               'Вы можете продолжить пользоваться ботом, либо дождаться окончания генерации здесь.\n\n'
               f'🔔 Мы пришлём вам уведомление.')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'🏠 На Главную', callback_data='start')]
        ]
    )

    return Window(photo_id=photo_id, caption=caption, markup=markup)


async def get_generation_error_window() -> Window:
    photo_id = 'images/generation_error'
    caption = ('Мы не смогли создать достаточно качественное изображение с текущей фотографией,'
               'либо произошла непредвиденная ошибка.\n\n'
               'Мы уже разбираемся в проблеме, попробуйте снова немного позже, либо используйте другое фото.')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'✖️ Закрыть', callback_data='close_window')]
        ]
    )

    return Window(photo_id=photo_id, caption=caption, markup=markup)


async def get_generation_success_window(result_image: BytesIO) -> Window:
    photo_id = result_image
    caption = None
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'✖️ Закрыть', callback_data='close_window')]
        ]
    )

    return Window(photo_id=photo_id, caption=caption, markup=markup)

