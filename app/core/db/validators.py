import re

from tortoise.validators import RegexValidator


__all__ = ["EmailValidator"]


class EmailValidator(RegexValidator):
    EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def __init__(self, flags: int | re.RegexFlag):
        super().__init__(self.EMAIL_PATTERN, flags)
