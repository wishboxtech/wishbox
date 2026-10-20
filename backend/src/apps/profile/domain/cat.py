from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Variant = Annotated[int, Field(strict=True, ge=0, le=49)]


class CatAvatar(BaseModel):
    """Versioned vector cat recipe; all layers share one coordinate system."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    version: Annotated[int, Field(strict=True, ge=1, le=1)] = 1
    face: Variant = 0
    ears: Variant = 0
    eyes: Variant = 0
    pupils: Variant = 0
    brows: Variant = 0
    nose: Variant = 0
    mouth: Variant = 0
    whiskers: Variant = 0
    markings: Variant = 0
    accessories: Variant = 0
    fur: Annotated[int, Field(strict=True, ge=0, le=15)] = 0
    background: Annotated[int, Field(strict=True, ge=0, le=11)] = 0
