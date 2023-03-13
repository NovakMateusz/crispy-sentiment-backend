import sanic

from app.service.blueprints import information_blueprint, prediction_blueprint
from app.service.listeners import download_artifacts, load_ml_model, setup_sentence_splitter
from app.service.middlewares import (
    set_cors_headers_on_response,
    set_x_request_id_on_request,
    set_x_request_id_on_response,
)
from app.service.settings import Settings

__all__ = ["create_app"]


def _register_blueprints(app: sanic.Sanic) -> None:
    api = sanic.Blueprint.group([prediction_blueprint, information_blueprint], version_prefix="/api/v")
    app.blueprint(api)


def _register_listeners(app: sanic.Sanic) -> None:
    app.register_listener(download_artifacts, "before_server_start")
    app.register_listener(load_ml_model, "before_server_start")
    app.register_listener(setup_sentence_splitter, "before_server_start")


def _register_middlewares(app: sanic.Sanic) -> None:
    app.register_middleware(set_cors_headers_on_response, "response")
    app.register_middleware(set_x_request_id_on_request, "request")
    app.register_middleware(set_x_request_id_on_response, "response")


def create_app() -> sanic.Sanic:
    app = sanic.Sanic(name=Settings.APP_NAME)
    app.update_config(Settings)

    _register_blueprints(app)
    _register_listeners(app)
    _register_middlewares(app)

    return app
