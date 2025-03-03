import csv
import io
from ..producers.products_load_producer import ProductsLoadProducer

class ProcessFile:

    def __init__(self):
        self.producer = ProductsLoadProducer()

    def execute(self, file):
        products = []
        # Decode the file stream to a text stream
        text_stream = io.TextIOWrapper(file.stream, encoding='utf-8')
        csv_reader = csv.DictReader(text_stream)
        for row in csv_reader:
            products.append(row)
        # Here we would process the products
        self.producer.produce(products)
        return {"message": "File successfully uploaded and processed"}
