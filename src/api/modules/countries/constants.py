from enum import StrEnum


class Ecuador(StrEnum):
    """Enumeración del país Ecuador para normalización de direcciones."""

    ECUADOR = "Ecuador"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]
