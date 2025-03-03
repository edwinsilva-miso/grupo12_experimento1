class DeleteProduct:

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def execute(self, id: str) -> None:
        self.product_repository.delete(id)