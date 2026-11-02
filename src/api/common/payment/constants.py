from enum import Enum

PAYMENT_LINK_EMAIL_SUBJECT = "Confirmación y enlace de pago para su orden #{order_number} | Sacré"


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
