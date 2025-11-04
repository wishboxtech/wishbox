from typing import Optional
from pydantic import BaseModel


class GeneralFields(BaseModel):
    shape: str
    fill_color: Optional[str]


class Widgets(BaseModel):
    ear: GeneralFields
    face: GeneralFields
    tops: GeneralFields
    eyes: GeneralFields
    nose: GeneralFields
    mouth: GeneralFields
    beard: GeneralFields
    clothes: GeneralFields
    glasses: GeneralFields
    earrings: GeneralFields
    eyebrows: GeneralFields


class AvatarSettings(BaseModel):
    gender: str
    widgets: Widgets
