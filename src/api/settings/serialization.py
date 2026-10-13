from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

import orjson
from fastapi.responses import JSONResponse as BaseJSONResponse


def custom_serializer(obj: Any) -> Any:
    """Custom serializer for types not handled by orjson natively."""

    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        # Preserve precision as string to avoid floating point issues
        return str(obj)
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8")

    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


class JSONResponse(BaseJSONResponse):
    """
    High-performance JSON response using orjson.

    Features:
    - 10x faster than stdlib json.
    - Native support for datetime, UUID.
    - Proper Decimal handling.
    - UTF-8 output with proper formatting.
    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Render content to JSON bytes using orjson."""

        return orjson.dumps(
            content,
            default=custom_serializer,
            option=orjson.OPT_UTC_Z | orjson.OPT_NAIVE_UTC,
        )
