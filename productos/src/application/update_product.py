from ..domain.entities.product_dto import ProductDTO


class UpdateProduct:

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def execute(self, product: ProductDTO) -> ProductDTO:
        return self.product_repository.update(product)
