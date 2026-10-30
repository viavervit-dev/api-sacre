from enum import Enum, StrEnum

PAYMENT_LINK_EMAIL_SUBJECT = "Confirmación y enlace de pago para su orden #{order_number} | Sacré"


class PaymentType(StrEnum):
    """"""

    PAYMENT_LINK = "Link de pago"
    PAYMENT_GATEWAY = "Pasarela de pago"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


class PaymentEntity(Enum):
    """Metadatos asociados a la entidad `Payment`."""

    # Descripciones para los campos de la entidad
    STATUS_DESCRIPTION = "Estado actual de la orden de compra."
    TYPE_DESCRIPTION = "Medio de pago utilizado."
    PAYMENT_DESCRIPTION = "Breve descripción del propósito de la transacción."
    SHOPPING_ORDER_ID_DESCRIPTION = "Identificador único de la orden de compra."

    # Mensajes de error
    SHOPPING_ORDER_NOT_FOUND = "La orden de compra no existe."


class ExceptionErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error para excepciones
    del módulo de pagos.
    """

    GATEWAY_TIMEOUT = "El servicio de pagos tardó demasiado en responder."
    GATEWAY_CONNECTION_ERROR = "No se pudo conectar con el servicio de pagos."
    GATEWAY_CONFIG_ERROR = "Error interno de configuración con el servicio de pagos."
    GATEWAY_UNAVAILABLE = "El servicio de pagos no se encuentra disponible temporalmente."
    GATEWAY_REJECTED = "El servicio de pago rechazó la petición."
    GATEWAY_INVALID_RESPONSE = "Respuesta inválida de la pasarela."
    DELIVERY_ERROR = "Ocurrió un error al notificar al cliente de la transacción."
    ORDER_ALREADY_HAS_PAYMENT = (
        "La orden de compra ya tiene un enlace de pago o transacción asociada."
    )
