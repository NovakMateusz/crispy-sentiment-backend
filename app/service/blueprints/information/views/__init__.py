import sanic


__all__ = ["information_blueprint"]

information_blueprint = sanic.Blueprint("informations", version=1)


@information_blueprint.route("/information")
async def predict_view(request: sanic.Request) -> sanic.HTTPResponse:
    return sanic.json(request.app.ctx.predictor.get_info())
