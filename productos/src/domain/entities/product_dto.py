class ProductDTO:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __str__(self):
        return f'{self.id} - {self.name} - {self.price}'