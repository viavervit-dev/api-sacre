from dataclasses import dataclass
from decimal import Decimal
from typing import Final


@dataclass(frozen=True, slots=True)
class DecimalNumberConstants:
    """
    Reglas de dominio, límites técnicos y catálogo de errores para la entidad `DecimalNumber`.
    """

    class Limits:
        """Límites cuantitativos y restricciones técnicas para la entidad `DecimalNumber`."""

        MIN_LENGTH: int = 1
        MAX_LENGTH: int = 999
        MAX_DIGITS: int = 8
        DECIMAL_PLACES: int = 2
        MAX_VALUE: Decimal = Decimal(value="999999.99")
        MIN_VALUE: Decimal = Decimal(value="-999999.99")

    class Docs:
        """Descripciones y metadatos de documentación OpenAPI para la entidad `DecimalNumber`."""

        DESCRIPTION: str = "Valor numérico decimal."
        LIST_DESCRIPTION: str = "Lista de valores numéricos decimales."


DECIMAL_NUMBER_CONSTANTS: Final[DecimalNumberConstants] = DecimalNumberConstants()
