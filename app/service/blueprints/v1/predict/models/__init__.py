from typing import List
from uuid import UUID

from pydantic import BaseModel, field_serializer
from pydantic.fields import Field


__all__ = ["PredictInputModel", "PredictResponseModel", "SavePredictionInputModel"]


class PredictInputModel(BaseModel):
    text: str


class PredictResponseModel(BaseModel):
    start: int
    stop: int
    sentiment: str


class SavePredictionInputModel(BaseModel):
    raw_text: str = Field(alias="raw-text")
    annotations: List[PredictResponseModel]


class UserPredictionResponseModel(BaseModel):
    id: UUID
    text: str
    annotations: List[PredictResponseModel]

    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)
