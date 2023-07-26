import uuid

from fastapi import APIRouter, HTTPException, Request
from tortoise.transactions import in_transaction

from .models import LoginInputModel, LoginResponseModel, RegistrationInputModel, RegistrationResponseModel
from app.core.db.enums import UserStatusEnum
from app.core.db.models import Users
from app.core.security import check_password, hash_password

__all__ = ["router"]

router = APIRouter()


@router.post("/login", response_model=LoginResponseModel)
async def issue_token(body: LoginInputModel, request: Request) -> LoginResponseModel:
    user = await Users.filter(email=body.email, status=UserStatusEnum.ACTIVE).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    if not check_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = request.app.state.token_handler.generate_token(user_public_id=user.public_id)
    async with in_transaction() as async_connection:
        user.update_from_dict({"is_login": True})
        await user.save(using_db=async_connection)

    return LoginResponseModel(token=token)


@router.post("/register", response_model=RegistrationResponseModel)
async def register_user(body: RegistrationInputModel):
    if await Users.filter(email=body.email).first():
        return HTTPException(status_code=400, detail="User already exists")

    async with in_transaction() as async_connection:
        new_user = Users(
            public_id=uuid.uuid4(),
            email=body.email,
            password=hash_password(body.password),
            status=UserStatusEnum.ACTIVE,
        )
        await new_user.save(using_db=async_connection)
    return RegistrationResponseModel(message="ok")

@router.post("/logout", response_model=RegistrationResponseModel)
