from typing import Tuple

from PIL import Image

from app.assets.template_cropboxes import CROP_BOXES

BASE_PATH = '../../assets/templates'


def main(template_id: int, gender: str, crop_box: Tuple[int, int, int, int]) -> None:
    path = f'{BASE_PATH}/template_{template_id}'

    image = Image.open(f'{path}/{gender}.jpg')
    cropped_image = image.crop(crop_box)
    cropped_image.save(f'{path}/{gender}_cropped.jpg')


if __name__ == '__main__':
    for i in range(1):
        i += 12

        main(i, 'male', CROP_BOXES[f'template_{i}_male'])
        main(i, 'female', CROP_BOXES[f'template_{i}_female'])


    # TEMPLATE = 4
    # GENDER = ('man', 'woman')[1]
    #
    # LEFT = 1584
    # UP = 0
    # RIGHT = 2128
    # DOWN = 1120
    #
    # main(TEMPLATE, GENDER, (LEFT, UP, RIGHT, DOWN))
    # print(f'template_{TEMPLATE} for {GENDER.upper()} is ready!:\n{(LEFT, UP, RIGHT, DOWN)}')


