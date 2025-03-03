from ..database.declarative_base import Session
from ..model.product_model import ProductModel


class ProductDAO:

    @staticmethod
    def save(product: ProductModel) -> str:
        session = Session()
        session.add(product)
        session.commit()
        session.refresh(product)
        session.close()
        return product.id

    @staticmethod
    def find_all() -> list[ProductModel]:
        session = Session()
        products = session.query(ProductModel).all()
        session.close()
        return products

    @staticmethod
    def find_by_id(product_id: str) -> ProductModel:
        session = Session()
        product = session.query(ProductModel).filter(ProductModel.id == product_id).first()
        session.close()
        return product

    @staticmethod
    def update(product: ProductModel) -> ProductModel:
        session = Session()
        existing = session.query(ProductModel).filter(ProductModel.id == product.id).first()
        if existing:
            existing.name = product.name
            existing.price = product.price
            session.commit()
        session.close()
        return product

    @staticmethod
    def delete(product_id: str) -> None:
        session = Session()
        session.query(ProductModel).filter(ProductModel.id == product_id).delete()
        session.commit()
        session.close()
