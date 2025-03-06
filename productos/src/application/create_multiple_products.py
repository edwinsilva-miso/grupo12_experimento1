class CreateMultipleProducts:

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def execute(self, products) -> None:
        self.product_repository.save_all(products)