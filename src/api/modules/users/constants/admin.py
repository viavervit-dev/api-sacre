from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class AdminConstants:
    """Reglas de dominio, límites técnicos y catálogo de errores para la entidad `Admin`."""

    class Limits:
        """Límites cuantitativos y restricciones técnicas para la entidad `Admin`."""

        FIRST_NAMES_MAX_LENGTH: int = 40
        LAST_NAMES_MAX_LENGTH: int = 40

    class Docs:
        """Descripciones y metadatos de documentación OpenAPI para la entidad `Admin`."""

        FIRST_NAMES_DESCRIPTION: str = "Primer y segundo nombre del administrador."
        LAST_NAMES_DESCRIPTION: str = "Primer y segundo apellido del administrador."


ADMIN_CONSTANTS: Final[AdminConstants] = AdminConstants()
