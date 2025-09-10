from logging.config import dictConfig

from .log_definition import logging_config


def setup_logging():
    dictConfig(config=logging_config)
