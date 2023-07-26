from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.service.utils.lifespan_functions import (
    init_db,
    setup_jwt_handler,
    setup_predictor,
    setup_splitter,
    close_db_connection,
)
from app.service.routers import information, prediction, authentication
from app.settings import Settings

from app.utils.logger import get_app_logger


__all__ = ["create_app"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    logger = get_app_logger()
    app.state.logger = logger

    logger.info("Opening connection to the database")
    await init_db(settings=settings)

    logger.info("Setting up JWT Handler")
    setup_jwt_handler(settings=settings, app=app)

    logger.info("Loading ML model")
    await setup_predictor(settings=settings, app=app)

    model_info = app.state.predictor.get_info()
    logger.info("Model %s with hash %s loaded successfully", model_info["name"], model_info["hash"])

    logger.info("Loading Sentence Splitter")
    setup_splitter(settings=settings, app=app)

    yield

    logger.info("Closing connection to the database")
    await close_db_connection()


def _register_routers(app: FastAPI) -> None:
    app.include_router(information.router)
    app.include_router(prediction.router)
    app.include_router(authentication.router)


def _register_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    _register_routers(app)
    _register_middlewares(app)

    return app
