import uuid

import sanic
from sanic_ext import validate
from tortoise.transactions import in_transaction

from app.core.db.enums import UserStatusEnum
from app.core.db.models import Users
from app.core.security import check_password, hash_password
from app.service.blueprints.authentication.models import RegistrationInputModel, LoginInputModel
from app.service.utils.decorators import authorized


__all__ = ["authentication_blueprint"]

authentication_blueprint = sanic.Blueprint("authentication", version=1, url_prefix="auth")


@authentication_blueprint.route("/login", methods=["POST"])
@validate(json=LoginInputModel)
async def login_view(request: sanic.Request, body: LoginInputModel) -> sanic.HTTPResponse:
    payload = body.dict()
    user = await Users.filter(email=payload["email"], status=UserStatusEnum.ACTIVE).first()
    if not user:
        return sanic.json({"message": "Incorrect credentials"}, 401)

    if not check_password(payload["password"], user.password):
        return sanic.json({"message": "Incorrect credentials"}, 401)

    token = request.app.ctx.token_handler.generate_token(user_public_id=user.public_id)
    async with in_transaction() as async_connection:
        user.update_from_dict({"is_login": True})
        await user.save(using_db=async_connection)

    return sanic.json({"token": token}, 200)


@authentication_blueprint.route("/register", methods=["POST"])
@validate(json=RegistrationInputModel)
async def register_view(_: sanic.Request, body: RegistrationInputModel) -> sanic.HTTPResponse:
    payload = body.dict()

    if await Users.filter(email=payload["email"]).first():
        return sanic.json({"message": "User already exists"}, 400)

    async with in_transaction() as async_connection:
        new_user = Users(
            public_id=uuid.uuid4(),
            email=payload["email"],
            password=hash_password(payload["password"]),
            status=UserStatusEnum.ACTIVE,
        )
        await new_user.save(using_db=async_connection)

    return sanic.json({})


@authentication_blueprint.route("/logout", methods=["POST"])
@authorized()
async def logout_view(_: sanic.Request, user_id: int):
    user = await Users.filter(id=user_id).first()
    async with in_transaction() as async_connection:
        user.update_from_dict({"is_login": False})
        await user.save(using_db=async_connection)
    return sanic.json({}, 200)
