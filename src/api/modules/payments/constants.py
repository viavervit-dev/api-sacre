from enum import Enum


class PaymentEntity(Enum):
    """Metadatos asociados a la entidad `Payment`."""

    # Descripciones para los campos de la entidad
    STATUS_DESCRIPTION = "Estado actual de la orden de compra."
    TYPE_DESCRIPTION = "Medio de pago utilizado."
