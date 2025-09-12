import uuid

from fastapi import HTTPException

from infrastructure.errors import ConversionUUIDError
from infrastructure.utils.converters import convert_str_to_uuid


def get_uuid(id: str) -> uuid.UUID:
    try:
        return convert_str_to_uuid(id)
    except ConversionUUIDError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
