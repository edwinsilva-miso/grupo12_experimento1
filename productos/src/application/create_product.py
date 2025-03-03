from ..domain.entities.product_dto import ProductDTO


class CreateProduct:

    def __init__(self, product_repository):
        self.product_repository = product_repository


    def execute(self, product: ProductDTO) -> str:
        return self.product_repository.add(product)