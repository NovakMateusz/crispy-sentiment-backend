import sanic

from service.blueprints import prediction_blueprint
from service.listeners import download_artifacts, load_ml_model
from service.settings import Settings

__all__ = ["create_app"]


def _register_blueprints(app: sanic.Sanic) -> None:
    api = sanic.Blueprint.group([prediction_blueprint], version_prefix="/api/v")

    app.blueprint(api)


def _register_listeners(app: sanic.Sanic) -> None:
    app.register_listener(download_artifacts, 'after_server_start')
    app.register_listener(load_ml_model, 'after_server_start')


def create_app() -> sanic.Sanic:
    app = sanic.Sanic(__name__)
    app.update_config(Settings)

    _register_blueprints(app)
    _register_listeners(app)

    return app
