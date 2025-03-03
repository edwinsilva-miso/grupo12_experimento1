from ...domain.entities.product_dto import ProductDTO
from ..model.product_model import ProductModel


class ProductMapper:

    @staticmethod
    def to_domain(product_dto: ProductDTO) -> ProductModel | None:
        if product_dto is None:
            return None

        return ProductModel(
            id = product_dto.id,
            name = product_dto.name,
            price = product_dto.price
        )

    @staticmethod
    def to_dto(product: ProductModel) -> ProductDTO | None:
        if product is None:
            return None

        return ProductDTO(
            product.id,
            product.name,
            product.price
        )

    @staticmethod
    def to_domain_list(products_dto: list[ProductDTO]) -> list[ProductModel]:
        return [ProductMapper.to_domain(product) for product in products_dto]

    @staticmethod
    def to_dto_list(products: list[ProductModel]) -> list[ProductDTO]:
        return [ProductMapper.to_dto(product) for product in products]
