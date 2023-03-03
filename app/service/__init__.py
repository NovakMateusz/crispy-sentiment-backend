import sanic

from app.service.blueprints import prediction_blueprint
from app.service.listeners import download_artifacts, load_ml_model, setup_sentence_splitter
from app.service.settings import Settings

__all__ = ["create_app"]


def _register_blueprints(app: sanic.Sanic) -> None:
    api = sanic.Blueprint.group([prediction_blueprint], version_prefix="/api/v")

    app.blueprint(api)


def _register_listeners(app: sanic.Sanic) -> None:
    app.register_listener(download_artifacts, "after_server_start")
    app.register_listener(load_ml_model, "after_server_start")
    app.register_listener(setup_sentence_splitter, "after_server_start")


def create_app() -> sanic.Sanic:
    app = sanic.Sanic(name=Settings.APP_NAME)
    app.update_config(Settings)

    _register_blueprints(app)
    _register_listeners(app)

    return app
