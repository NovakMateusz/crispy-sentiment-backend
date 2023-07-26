from pydantic import BaseModel

__all__ = ["PredictInputModel", "PredictResponseModel"]


class PredictInputModel(BaseModel):
    text: str


class PredictResponseModel(BaseModel):
    start: int
    stop: int
    sentiment: str
