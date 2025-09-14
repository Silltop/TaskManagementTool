import uuid
from datetime import datetime

from infrastructure.errors import ConversionUUIDError, DateConversionError


def convert_to_uuid(id_str: str) -> uuid.UUID:
    try:
        return uuid.UUID(id_str)
    except ValueError as e:
        raise ConversionUUIDError(f"Invalid UUID string: {id_str}") from e


def convert_to_datetime(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError as e:
        raise DateConversionError(f"Invalid datetime string: {date_str}") from e
