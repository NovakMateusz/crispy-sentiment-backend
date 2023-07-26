from enum import Enum

__all__ = ["UserStatusEnum", "PredictionAnnotationSentimentValueEnum"]


class UserStatusEnum(str, Enum):
    DISABLED = "disabled"
    ACTIVE = "active"
    BLOCKED = "blocked"


class PredictionAnnotationSentimentValueEnum(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
