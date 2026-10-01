from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.response import Response
from src.common.schema import response_scheme_400, response_scheme_503
from src.modules.auth.dto import ReadUserDTO
from src.modules.users.dependencies import get_create_customer_service
from src.modules.users.dto import CreateCustomerDTO
from src.modules.users.services.customers.create_customer import CreateCustomerService

create_customer_router = APIRouter(prefix="/users", tags=["Usuarios"])


@create_customer_router.post(
    path="/customer/",
    response_description="**(CREATED)** Cliente creado exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=CreateCustomerDTO),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def create_customer(
    service: Annotated[CreateCustomerService, Depends(get_create_customer_service)],
    data: CreateCustomerDTO,
) -> Response[ReadUserDTO]:
    """
    Registra un nuevo cliente en el sistema y crea su cuenta de usuario.

    ### Descripción
    Crea una cuenta de usuario con rol de cliente y su perfil asociado con datos
    personales, de identificación y de contacto. Ejecuta validaciones sintácticas y de negocio
    para garantizar la unicidad de las credenciales y documentos, encripta la contraseña de forma
    segura y asigna automáticamente los permisos correspondientes al rol.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación previa.

    ### Flujo de Ejecución
    1. **Validación Sintáctica (DTO):**
        - Valida el formato de correo electrónico, longitud de contraseña, límites de texto y
         tipos de documento permitidos.
    2. **Validaciones de Reglas de Negocio:**
        - **Unicidad de Correo:** Comprueba que el correo electrónico no esté registrado.
        - **Unicidad de Teléfono:** Comprueba que el número de teléfono no esté en uso.
        - **Unicidad de Documento:** Comprueba que el número de documento no esté registrado.
    3. **Creación de Cuenta Base de Usuario:**
        - Asigna el rol de cliente (`customer`).
        - Encripta la contraseña mediante hashing seguro (bcrypt).
        - Asocia el grupo y los permisos correspondientes.
    4. **Creación del Perfil de Cliente:**
        - Registra los datos personales y de identificación, vinculándolos mediante clave foránea
         (`user_id`) a la cuenta de usuario creada.
    5. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    customer = await service.create_customer(data=data)

    return Response(
        success=True,
        pagination=False,
        message="Cliente creado exitosamente.",
        data=customer,
    )
