import sanic
from tortoise.contrib.sanic import register_tortoise

from app.settings import Settings
from app.service.blueprints import v1
from app.service.utils.middlewares import (
    set_cors_headers_on_options_request,
    set_cors_headers_on_response,
    set_corelation_id_on_request,
    set_corelation_id_on_response,
)
from app.service.utils.listeners import setup_token_handler, load_ml_model, setup_splitter


def _register_blueprints(app: sanic.Sanic) -> None:
    v1_group = sanic.Blueprint.group(v1.auth.blueprint, v1.info.blueprint, v1.predict.blueprint, url_prefix="/v1")
    app.blueprint(v1_group)


def _register_middlewares(app: sanic.Sanic) -> None:
    app.register_middleware(set_corelation_id_on_request, "request")
    app.register_middleware(set_cors_headers_on_options_request, "request")
    app.register_middleware(set_cors_headers_on_response, "response")
    app.register_middleware(set_corelation_id_on_response, "response")


def _register_listeners(app: sanic.Sanic) -> None:
    app.register_listener(setup_token_handler, "before_server_start")
    app.register_listener(load_ml_model, "before_server_start")
    app.register_listener(setup_splitter, "before_server_start")


def create_app() -> sanic.Sanic:
    app = sanic.Sanic(name=Settings.APP_NAME)
    app.update_config(Settings)

    _register_blueprints(app=app)
    _register_middlewares(app=app)
    _register_listeners(app=app)

    register_tortoise(
        app=app,
        modules={"models": ["app.core.database.models"]},
        db_url=Settings.DB_URL,
        generate_schemas=Settings.GENERATE_DB_SCHEMAS,
    )

    return app
