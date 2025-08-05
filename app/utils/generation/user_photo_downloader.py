from io import BytesIO
from app.config import bot


async def get_user_photo(file_id: str) -> list:
    try:
        file = await bot.get_file(file_id)
        file_data = await bot.download_file(file.file_path)
        result = BytesIO(file_data.read())

        if not result:
            raise Exception

        return ['SUCCESS', result]

    except Exception as ex:
        return ['ERROR', ex]