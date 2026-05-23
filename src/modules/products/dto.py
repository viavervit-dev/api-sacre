from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import DTOValidationErrorMessages
from src.modules.products.constants import CategoryEntity
from src.modules.products.repositories.interfaces import IProductRepository


class CreateCategoryDTO(BaseModel):
    """DTO para la creación de una categoria de producto."""

    name: str = Field(
        max_length=CategoryEntity.NAME_MAX_LENGTH.value,
        description=CategoryEntity.NAME_DESCRIPTION.value,
        examples=["Rosarios"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                CategoryEntity.NAME_IN_USE.value,
            ]
        },
    )
    description: str = Field(
        max_length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value,
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )

    async def check_name(
        self,
        session: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el nombre de la categoría."""

        # Validar que el nombre de la categoría no esté registrado en la base de datos
        exists = await product_repo.exists_category(session=session, filters={"name": self.name})

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "name"),
                        "msg": CategoryEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )


class ReadCategoryDTO(BaseModel):
    """DTO para la lectura de una categoría de producto."""

    id: UUID = Field(
        description=CategoryEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name: str = Field(
        description=CategoryEntity.NAME_DESCRIPTION.value,
        examples=["Rosarios"],
    )
    description: str = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
    )
    product_count: int = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[10, 15],
    )
    status: bool = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[True, False],
    )
