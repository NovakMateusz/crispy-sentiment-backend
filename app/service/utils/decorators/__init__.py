import functools
from typing import Any, Awaitable, Callable, Dict, List

import jwt
import sanic
from tortoise.transactions import in_transaction
from pydantic import BaseModel, ValidationError

from app.core.database.models import Users
from app.core.database.enums import UserStatusEnum

__all__ = ["authorized", "validate"]


def authorized():
    def decorator(view_function: Callable[[Any, Any], Awaitable[Any]]):
        @functools.wraps(view_function)
        async def decorated_function(request: sanic.Request, *args: List[Any], **kwargs: Dict[Any, Any]):
            try:
                token = request.headers["Authorization"]
                user_public_id = request.app.ctx.token_handler.validate_token(token=token)
            except KeyError:
                return sanic.json({"message": "Missing token"}, 401)

            except jwt.exceptions.ExpiredSignatureError:
                user_public_id = request.app.ctx.token_handler.validate_token(
                    token=request.token, verify_signature=False
                )
                user = await Users.filter(public_id=user_public_id, status=UserStatusEnum.ACTIVE).first()
                if user and user.is_login:
                    async with in_transaction() as async_connection:
                        user.update_from_dict({"is_login": False})
                        await user.save(using_db=async_connection)
                return sanic.json({"message": "Token expired"}, 401)

            except (
                ValueError,
                jwt.exceptions.DecodeError,
                jwt.exceptions.InvalidIssuerError,
                jwt.exceptions.InvalidSignatureError,
            ):
                return sanic.json({"message": "Invalid token"}, 401)

            user = await Users.filter(public_id=user_public_id, status=UserStatusEnum.ACTIVE, is_login=True).first()
            if not user:
                # Log event - token for logout user has been used
                return sanic.json({"message": "Invalid token"}, 401)

            response = await view_function(request, user, *args, **kwargs)
            return response

        return decorated_function
    return decorator


def validate(model: BaseModel):
    def decorator(view_function: Callable[[Any, Any], Awaitable[Any]]):
        @functools.wraps(view_function)
        async def decorated_function(request: sanic.Request, *args: List[Any], **kwargs: Dict[Any, Any]):
            try:
                input_model = model(**request.json)
            except (TypeError, ValidationError):
                return sanic.json({"message": "Incorrect payload"}, 400)
            response = await view_function(request, input_model, *args, **kwargs)
            return response
        return decorated_function
    return decorator
