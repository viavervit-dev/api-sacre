from decimal import Decimal

TWO_DECIMAL_PLACES = Decimal("0.01")
TAX_PERCENTAGE = Decimal("0.1500")


PAGINATION_OFFSET_DESCRIPTION = (
    "Define la cantidad de registros que se saltarán desde el inicio "
    "de la lista ordenada. Un valor de `0` significa que iniciará "
    "desde el primer registro disponible."
)
PAGINATION_LIMIT_DESCRIPTION = (
    "Define la cantidad máxima de registros a retornar en la respuesta "
    "actual. Útil para determinar el tamaño de la página."
)
