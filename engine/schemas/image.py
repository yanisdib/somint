from pydantic import BaseModel


class CropRegion(BaseModel):
    """A model to represent a rectangular region for cropping using start and end coordinates."""

    x_start: int
    x_end: int
    y_start: int
    y_end: int
