from ..domain.entities.product_dto import ProductDTO

class GetAllProducts:

    def __init__(self, product_repository):
        self.product_repository = product_repository


    def execute(self) -> list[ProductDTO]:
        return self.product_repository.get_all()