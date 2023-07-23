import functools

import jwt
import sanic

from app.core.db.models import Users
from app.core.db.enums import UserStatusEnum

__all__ = ["authorized"]


def authorized():
    def decorator(view_function):
        @functools.wraps(view_function)
        async def decorated_function(request: sanic.Request, *args, **kwargs):
            try:
                user_public_id = request.app.ctx.token_handler.validate_token(token=request.token)
            except jwt.exceptions.ExpiredSignatureError:
                return sanic.json({"message": "Token expired"}, 401)
            except (
                ValueError,
                jwt.exceptions.DecodeError,
                jwt.exceptions.InvalidIssuerError,
                jwt.exceptions.InvalidSignatureError,
            ):
                return sanic.json({"message": "Invalid token"}, 401)

            user = await Users.filter(
                public_id=user_public_id, status=UserStatusEnum.ACTIVE, is_login=True
            ).first()
            if not user:
                # Log event - token for logout user has been used
                return sanic.json({"message": "Invalid token"}, 401)

            response = await view_function(request, user.id, *args, **kwargs)
            return response

        return decorated_function

    return decorator
