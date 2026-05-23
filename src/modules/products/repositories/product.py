from src.modules.products.repositories.category import CategoryRepository
from src.modules.products.repositories.interfaces import IProductRepository


class ProductRepository(IProductRepository, CategoryRepository):
    """
    Repositorio para productos. Esta clase proporciona métodos que realizan operaciones en la tabla
    `product.products` de la base de datos, resuelve dinámicamente las consultas y relaciones.
    """

    pass
