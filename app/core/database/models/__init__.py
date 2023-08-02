import re

from tortoise.models import Model
from tortoise import fields

from app.core.database.enums import UserStatusEnum, PredictionAnnotationSentimentValueEnum
from app.core.database.validators import EmailValidator

__all__ = ["Users", "Predictions", "PredictionAnnotations"]


class Users(Model):
    id = fields.IntField(pk=True)
    public_id = fields.UUIDField()
    email = fields.CharField(100, unique=True, validators=[EmailValidator(re.VERBOSE)])
    password_hash = fields.CharField(max_length=128)
    status = fields.CharEnumField(UserStatusEnum)
    is_login = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    predictions: fields.ReverseRelation["Predictions"]


class Predictions(Model):
    id = fields.UUIDField(pk=True)
    user: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField("models.Users", related_name="predictions")
    raw_text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    prediction_annotations: fields.ReverseRelation["PredictionAnnotations"]


class PredictionAnnotations(Model):
    id = fields.IntField(pk=True)
    prediction: fields.ForeignKeyRelation[Predictions] = fields.ForeignKeyField(
        "models.Predictions", related_name="prediction_annotations"
    )
    sentiment = fields.CharEnumField(PredictionAnnotationSentimentValueEnum)
    start = fields.IntField()
    stop = fields.IntField()
