from typing import Dict, Optional

from pydantic import BaseModel, EmailStr, validator
from pydantic.fields import Field

__all__ = ["LoginInputModel", "LoginResponseModel", "RegistrationInputModel", "RegistrationResponseModel"]


class LoginInputModel(BaseModel):
    email: EmailStr
    password: str


class LoginResponseModel(BaseModel):
    token: str


class RegistrationInputModel(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str = Field(alias="password-repeat")

    @validator("password_repeat")
    def password_match(cls, v: str, values: Dict[str, str]) -> Optional[str]:
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords must match")
        return v


class RegistrationResponseModel(BaseModel):
    message: str
