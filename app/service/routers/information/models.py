from pydantic import BaseModel, validator

__all__ = ["InformationResponseModel", "ModelMetrics"]


class ModelMetrics(BaseModel):
    precision: float
    recall: float
    f1: float

    @validator("precision", "recall", "f1")
    def float_round(cls, value: float) -> float:
        return round(value, 2)


class InformationResponseModel(BaseModel):
    name: str
    hash: str
    metrics: ModelMetrics

    @validator("name")
    def parse_model_name(cls, value: str) -> str:
        return " ".join(value.split("_")).title()
