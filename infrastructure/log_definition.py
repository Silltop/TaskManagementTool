logging_config = {
    "version": 1,
    "formatters": {
        "detailed": {
            "()": "infrastructure.log_config.ColorFormatter",
            "format": "[%(asctime)s | %(levelname)s | %(processName)s:%(process)d | line:%(lineno)d] | %(name)s | %(module)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "detailed",
            "level": "INFO",
        },
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout"]},
        "uvicorn": {"level": "INFO", "propagate": True},
        "uvicorn.error": {"level": "INFO", "propagate": True},
        "uvicorn.access": {"level": "INFO", "propagate": True},
        "uvicorn.asgi": {"level": "INFO", "propagate": True},
    },
}
