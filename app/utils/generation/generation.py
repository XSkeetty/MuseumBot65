from app.models.database import User as DB_User
from app.requests.rp_requests import face_swap
from app.utils.generation.image_restore import restore_photo
from app.utils.generation.user_photo_downloader import get_user_photo


async def generation_start(db_user: DB_User) -> list:
    try:
        user_photo = await get_user_photo(db_user.last_photo_id)
        if user_photo[0] == 'ERROR':
            return ['ERROR', 'GET_PHOTO', user_photo[1]]

        cropped_user_photo = await face_swap(db_user.template_id, user_photo[1], db_user.gender)
        if cropped_user_photo[0] == 'ERROR':
            return cropped_user_photo

        result = await restore_photo(db_user.template_id, db_user.gender, cropped_user_photo[1])
        if not result:
            return ['ERROR', 'RESTORE_PHOTO', result[1]]

        return ['SUCCESS', result[1]]

    except Exception as ex:
        return ['ERROR', f'{ex}']

