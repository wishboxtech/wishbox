from typing import Optional

from pydantic import BaseModel


class Background(BaseModel):
    color: str
    border_color: str


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
    wrapper_shape: str
    background: Background
    gender: str
    widgets: Widgets
