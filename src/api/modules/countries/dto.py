from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.users.constants import Ecuador


class ReadCountryDTO(BaseModel):
    """DTO para la lectura y respuesta de datos básicos de un país."""

    name: str = Field(
        description="Nombre del país.",
        examples=["Ecuador"],
    )
    code: str = Field(
        description="Código del país.",
        examples=["EC"],
    )


class ReadAdministrativeStructureDTO(BaseModel):
    """DTO para la lectura de la organización territorial de un país."""

    administrative_structure: dict[str, Any] = Field(
        description="Estructura y organización territorial del país.",
        examples=[
            {
                "Provincia": {
                    "Pichincha": {
                        "Canton": {
                            "Quito": {
                                "Ciudad": [
                                    "Quito",
                                    "Calacalí",
                                    "Calderón",
                                    "El Quinche",
                                    "La Merced",
                                    "Lloa",
                                ]
                            },
                            "Rumiñahui": {
                                "Ciudad": [
                                    "Sangolquí",
                                    "San Pedro de Taboada",
                                    "Cotogchoa",
                                    "San Rafael",
                                    "Rumipamba",
                                ]
                            },
                        }
                    }
                }
            }
        ],
    )


class LocationEcuadorDTO(BaseModel):
    """DTO para los datos de ubicación geográfica y dirección en Ecuador."""

    model_config = ConfigDict(use_enum_values=True)

    country: Ecuador = Field(
        description="Nombre del país.",
        examples=Ecuador.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.ENUM.value,
            ]
        },
    )
    province: str = Field(
        max_length=100,
        description="Nombre oficial de la provincia.",
        examples=["Pichincha"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    canton: str = Field(
        max_length=100,
        description="Nombre oficial del cantón.",
        examples=["Quito"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    city: str = Field(
        max_length=100,
        description="Nombre oficial de la ciudad o localidad.",
        examples=["Zámbiza"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    address: str = Field(
        max_length=100,
        description="Dirección de entrega.",
        examples=["Manzana 12 casa 32"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )


class ReadLocationEcuadorDTO(BaseModel):
    """DTO de lectura para los datos de ubicación geográfica y dirección en Ecuador."""

    model_config = ConfigDict(use_enum_values=True)

    country: Ecuador = Field(
        description="Nombre del país.",
        examples=Ecuador.values(),
    )
    province: str = Field(
        description="Nombre oficial de la provincia.",
        examples=["Pichincha"],
    )
    canton: str = Field(
        description="Nombre oficial del cantón.",
        examples=["Quito"],
    )
    city: str = Field(
        description="Nombre oficial de la ciudad o localidad.",
        examples=["Zámbiza"],
    )
    address: str = Field(
        description="Dirección de entrega.",
        examples=["Manzana 12 casa 32"],
    )
