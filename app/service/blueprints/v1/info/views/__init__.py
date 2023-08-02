from sanic import Blueprint, Request, HTTPResponse, json

from app.service.blueprints.v1.info.models import InformationResponseModel


__all__ = ["blueprint"]

blueprint = Blueprint("info")


@blueprint.route('/info', methods=["GET", "OPTIONS"])
async def info_view(request: Request) -> HTTPResponse:
    return json(InformationResponseModel(**request.app.ctx.predictor.get_info()).model_dump())
