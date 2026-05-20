from pydantic import BaseModel, Field

from src.modules.admins.constants import AdminEntity


class ReadAdminDTO(BaseModel):
    """DTO para la lectura de datos de un administrador."""

    first_names: str = Field(
        description=AdminEntity.FIRST_NAMES_DESCRIPTION.value,
        examples=["Juan Pablo"],
    )
    last_names: str = Field(
        description=AdminEntity.LAST_NAMES_DESCRIPTION.value,
        examples=["Pérez Gómez"],
    )
