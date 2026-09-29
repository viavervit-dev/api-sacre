from enum import Enum


class CountryEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Country`."""

    # Descripciones para los campos de la entidad
    NAME_DESCRIPTION = "Nombre del país."
    ADMINISTRATIVE_STRUCTURE_DESCRIPTION = "Estructura y organización territorial del país."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 60
