from typing import Any

from pydantic import BaseModel, Field


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
