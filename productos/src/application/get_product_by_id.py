from ..domain.entities.product_dto import ProductDTO

class GetProductById:

    def __init__(self, product_repository):
        self.product_repository = product_repository


    def execute(self, id: str) -> ProductDTO:
        return self.product_repository.get_by_id(id)