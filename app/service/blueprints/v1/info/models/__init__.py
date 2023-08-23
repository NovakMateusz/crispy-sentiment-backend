from pydantic import BaseModel, validator

__all__ = ["InformationResponseModel", "ModelMetrics", "SingleDocumentationModel", "ExtraDocumentationModel"]


class ModelMetrics(BaseModel):
    precision: float
    recall: float
    f1: float

    @validator("precision", "recall", "f1")
    def float_round(cls, value: float) -> float:
        return round(value, 2)


class SingleDocumentationModel(BaseModel):
    text: str
    source: str


class ExtraDocumentationModel(BaseModel):
    model: SingleDocumentationModel
    precision: SingleDocumentationModel
    recall: SingleDocumentationModel
    f1: SingleDocumentationModel


class InformationResponseModel(BaseModel):
    name: str
    hash: str
    metrics: ModelMetrics
    documentation: ExtraDocumentationModel | None = None

    @validator("name")
    def parse_model_name(cls, value: str) -> str:
        return " ".join(value.split("_")).title()
