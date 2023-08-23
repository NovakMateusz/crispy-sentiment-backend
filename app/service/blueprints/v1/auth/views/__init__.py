import uuid

import sanic
from tortoise.transactions import in_transaction

from app.core.database.enums import UserStatusEnum
from app.core.database.models import Users
from app.core.security import check_password, hash_password
from app.service.blueprints.v1.auth.models import LoginInputModel, RegistrationInputModel
from app.service.utils.decorators import authorized

__all__ = ["blueprint"]

blueprint = sanic.Blueprint("auth")


@blueprint.route("/login", methods=["POST", "OPTIONS"])
async def login_view(request: sanic.Request) -> sanic.HTTPResponse:
    input_model = LoginInputModel(**request.json)
    user = await Users.filter(email=input_model.email, status=UserStatusEnum.ACTIVE).first()
    if not user:
        return sanic.json({"message": "Incorrect credentials"}, 401)

    if not check_password(input_model.password, user.password_hash):
        return sanic.json({"message": "Incorrect credentials"}, 401)

    token = request.app.ctx.token_handler.generate_token(user_public_id=user.public_id)
    async with in_transaction() as async_connection:
        user.update_from_dict({"is_login": True})
        await user.save(using_db=async_connection)

    return sanic.json({"token": token}, 200)


@blueprint.route("/register", methods=["POST", "OPTIONS"])
async def register_view(request: sanic.Request) -> sanic.HTTPResponse:
    input_model = RegistrationInputModel(**request.json)
    if await Users.filter(email=input_model.email).first():
        return sanic.json({"message": "User already exists"}, 400)

    async with in_transaction() as async_connection:
        new_user = Users(
            public_id=uuid.uuid4(),
            email=input_model.email,
            password_hash=hash_password(input_model.password),
            status=UserStatusEnum.ACTIVE,
        )
        await new_user.save(using_db=async_connection)

    return sanic.json({"message": "User created"})


@blueprint.route("/logout", methods=["POST", "OPTIONS"])
@authorized()
async def logout_view(_: sanic.Request, user: Users):
    async with in_transaction() as async_connection:
        user.update_from_dict({"is_login": False})
        await user.save(using_db=async_connection)
    return sanic.json({"message": "User logout"}, 200)
