from typing import Union
import uuid
from datetime import datetime, timezone

from infrastructure.errors import ConversionUUIDError, DateConversionError


def convert_to_uuid(id_str: str) -> uuid.UUID:
    try:
        return uuid.UUID(id_str)
    except ValueError as e:
        raise ConversionUUIDError(f"Invalid UUID string: {id_str}") from e


def convert_to_datetime(date_str: Union[datetime, str]) -> datetime:
    try:
        """Convert to timezone-aware datetime in UTC."""
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))  # should return datetime
        else:
            dt = date_str

        if dt.tzinfo is None:  # make naive datetimes UTC
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt
    except ValueError as e:
        raise DateConversionError(f"Invalid datetime string: {date_str}") from e
