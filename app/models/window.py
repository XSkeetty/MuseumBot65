from dataclasses import dataclass
from typing import Optional

from aiogram.types import ReplyKeyboardMarkup


@dataclass()
class Window():
    photo_id: Optional[str]
    caption: Optional[str]
    markup: Optional[ReplyKeyboardMarkup]
