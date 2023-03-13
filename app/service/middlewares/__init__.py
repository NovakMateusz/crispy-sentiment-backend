import uuid

import sanic

from app.service.utils import add_cors_headers

__all__ = ["set_cors_headers_on_response", "set_x_request_id_on_request", "set_x_request_id_on_response"]


def set_cors_headers_on_response(request: sanic.Request, response: sanic.HTTPResponse) -> None:
    if request.route:
        if request.method != "OPTIONS":
            add_cors_headers(response, request.route.methods)


def set_x_request_id_on_request(request: sanic.Request) -> None:
    if "X-Request-ID" not in request.headers:
        request.headers["X-Request-ID"] = str(uuid.uuid4())


def set_x_request_id_on_response(request: sanic.Request, response: sanic.HTTPResponse) -> None:
    response.headers["X-Request-ID"] = request.headers["X-Request-ID"]
