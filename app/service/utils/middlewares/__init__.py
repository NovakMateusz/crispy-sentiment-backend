from typing import Dict, List
import uuid

import sanic


__all__ = [
    "set_cors_headers_on_response",
    "set_cors_headers_on_response",
    "set_corelation_id_on_request",
    "set_corelation_id_on_response",
]


def _generate_cors_headers(allowed_methods: List[str]) -> Dict[str, str]:
    return {
        "Access-Control-Allow-Methods": ",".join(allowed_methods),
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "Origin, Content-Type, Accept, Authorization, Corelation-Id",
    }


async def set_cors_headers_on_response(request: sanic.Request, response: sanic.HTTPResponse) -> None:
    if request.route:
        allowed_http_methods = [method for method in request.route.methods]
        response.headers.update(_generate_cors_headers(allowed_http_methods))


async def set_cors_headers_on_options_request(request: sanic.Request):
    if request.route and request.method == "OPTIONS":
        allowed_http_methods = [method for method in request.route.methods]
        response = sanic.HTTPResponse()
        response.headers.update(_generate_cors_headers(allowed_http_methods))
        return response


async def set_corelation_id_on_request(request: sanic.Request) -> None:
    if not request.headers.get("corelation-id"):
        request.headers["corelation-id"] = str(uuid.uuid4())


async def set_corelation_id_on_response(request: sanic.Request, response: sanic.HTTPResponse) -> None:
    response.headers["corelation-id"] = request.headers.get("corelation-id")
