import asyncio
from io import BytesIO

import replicate
import requests


def face_swap_sync(template_id: int, user_photo: BytesIO, gender: str) -> BytesIO:
    client = replicate.Client(api_token="r8_Y9xW6TEotx5vPBBkztUzgynuSSEvKij0BnM1u")
    model = 'cdingram/face-swap:d1d6ea8c8be89d664a07a457526f7128109dee7030fdac424788d762c71ed111'

    with open(f'app/assets/templates/template_{template_id}/{gender}_cropped.jpg', 'rb') as template:
        data = {
            'swap_image': user_photo,
            'input_image': template
        }

        response_link = client.run(model, input=data)
        response = requests.get(response_link)

    response_bytes = BytesIO(response.content)

    return response_bytes

async def face_swap(template_id: int, user_photo: str, gender: str) -> list:
    try:
        result = await asyncio.to_thread(face_swap_sync, template_id, user_photo, gender)

        if result:
            return ['SUCCESS', result]
        else:
            return ['ERROR', 'FACE_SWAP_NULL']
    except Exception as ex:
        if 'No scheme supplied' in str(ex):
            return ['ERROR', 'FACE_SWAP_NULL']
        return ['ERROR', f'FACE_SWAP_{ex}']







