from io import BytesIO

from PIL import Image

from app.assets.template_cropboxes import CROP_BOXES


async def restore_photo(template_id: int, gender: str, cropped_user_photo: BytesIO) -> list:
    try:
        x1, y1, x2, y2 = CROP_BOXES[f'template_{template_id}_{gender}']

        original_template = Image.open(f'app/assets/templates/template_{template_id}/{gender}.jpg')
        user_photo = Image.open(cropped_user_photo).resize((x2 - x1, y2 - y1))
        original_template.paste(user_photo, (x1, y1))

        output_buffer = BytesIO()
        original_template.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        if not output_buffer:
            raise Exception

        return ['SUCCESS', output_buffer]

    except Exception as ex:
        return ['ERROR', ex]



