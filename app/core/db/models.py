import re

from tortoise import fields
from tortoise.models import Model

from .validators import EmailValidator
from .enums import UserStatusEnum, PredictionAnnotationSentimentValueEnum


__all__ = ["Users"]  # "Predictions", "PredictionAnnotations"]


class Users(Model):
    id = fields.IntField(pk=True)
    public_id = fields.UUIDField()
    email = fields.CharField(100, unique=True, validators=[EmailValidator(re.VERBOSE)])
    password_hash = fields.CharField(max_length=128, null=True)
    status = fields.CharEnumField(UserStatusEnum)
    is_login = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    # predictions: fields.ReverseRelation["Predictions"]

    class Meta:
        table = "users"


# class Predictions(Model):
#     id = fields.IntField(pk=True)
#     user: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField("models.Users", related_name="predictions")
#     raw_text = fields.TextField()
#     created_at = fields.DatetimeField(auto_now_add=True)

#     prediction_annotations: fields.ReverseRelation["PredictionAnnotations"]

#     class Meta:
#         table = "predictions"


# class PredictionAnnotations(Model):
#     id = fields.IntField(pk=True)
#     prediction: fields.ForeignKeyRelation[Predictions] = fields.ForeignKeyField(
#         "models.Predictions", related_name="prediction_annotations"
#     )
#     sentiment = fields.CharEnumField(PredictionAnnotationSentimentValueEnum)
#     start = fields.IntField()
#     stop = fields.IntField()

#     class Meta:
#         table = "prediction_annotations"
