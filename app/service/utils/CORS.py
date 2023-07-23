from typing import FrozenSet

import sanic


__all__ = ["add_cors_headers", "add_cors_headers_to_options"]


def add_cors_headers(response: sanic.HTTPResponse, methods: FrozenSet[str]) -> None:
    allow_methods = list(methods)
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ", ".join(allow_methods),
        "Access-Control-Allow-Origin": "http://localhost:8080",
        "Access-Control-Allow-Headers": "Origin, Content-Type, Accept, Authorization, X-XSRF-TOKEN, X-Request-ID",
    }

    response.headers.extend(headers)


def add_cors_headers_to_options(response: sanic.HTTPResponse, methods: FrozenSet[str]) -> None:
    allow_methods = list(methods)
    headers = {
        "Access-Control-Allow-Methods": ", ".join(allow_methods),
        "Access-Control-Allow-Origin": "http://localhost:8080",
        "Access-Control-Allow-Headers": "Origin, Content-Type, Accept, Authorization, X-XSRF-TOKEN, X-Request-ID",
        "Connection": "Keep-Alive",
    }
    response.headers.extend(headers)