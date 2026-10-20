from pydantic import BaseModel, ConfigDict


class AvatarValue(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class Background(AvatarValue):
    color: str
    border_color: str


class GeneralFields(AvatarValue):
    shape: str
    fill_color: str | None


class Widgets(AvatarValue):
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


class AvatarSettings(AvatarValue):
    wrapper_shape: str
    background: Background
    gender: str
    widgets: Widgets
