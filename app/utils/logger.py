import logging

__all__ = ["get_app_logger"]


def get_app_logger(logger_name: str = 'uvicorn') -> logging.Logger:
    return logging.getLogger(logger_name)
