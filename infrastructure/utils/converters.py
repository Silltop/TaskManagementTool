import uuid

from infrastructure.errors import ConversionUUIDError


def convert_str_to_uuid(id_str: str) -> uuid.UUID:
    try:
        return uuid.UUID(id_str)
    except ValueError as e:
        raise ConversionUUIDError(f"Invalid UUID string: {id_str}") from e
