import datetime
import uuid

import bcrypt
import jwt
import ujson

__all__ = ["hash_password", "check_password", "JWTHandler"]


def hash_password(password: str) -> str:
    hash_byte_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hash_byte_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(str.encode(password), str.encode(hashed_password))


class JWTHandler:
    algorithm = "HS256"

    def __init__(self, secret: str, issuer: str):
        self._secret = secret
        self._issuer = issuer

    def generate_token(self, user_public_id: uuid.uuid4) -> str:
        issue_at = datetime.datetime.now(tz=datetime.timezone.utc)
        expiration_time = issue_at + datetime.timedelta(hours=3)
        return jwt.encode(
            payload={
                "iat": issue_at,
                "exp": expiration_time,
                "iss": self._issuer,
                "sub": str(user_public_id),
            },
            key=self._secret,
            algorithm=self.algorithm,
        )

    def validate_token(self, token: str) -> uuid.UUID:
        payload = jwt.decode(
            jwt=token,
            key=self._secret,
            options={"require": ["iat", "exp", "iss", "sub"]},
            issuer=self._issuer,
            algorithms=[self.algorithm],
        )
        return uuid.UUID(payload["sub"])


# if __name__ == "__main__":
#     handler = JWTHandler("test", "backend")
#     user_id = uuid.uuid4()
#     token_123 = handler.generate_token(user_id)
#     try:
#         new_used_id = handler.validate_token(None)
#         assert user_id == new_used_id
#     except jwt.exceptions.ExpiredSignatureError as error:
#         print({"message": "Token expired"})
#     except (
#         ValueError,
#         jwt.exceptions.DecodeError,
#         jwt.exceptions.InvalidIssuerError,
#         jwt.exceptions.InvalidSignatureError,
#     ) as error:
#         print({"message": "Invalid token"})
