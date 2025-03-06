from ..database.declarative_base import Session
from ..model.product_model import ProductModel


class ProductDAO:

    @classmethod
    def save(cls, product: ProductModel) -> str:
        session = Session()
        session.add(product)
        session.commit()
        session.refresh(product)
        session.close()
        return product.id

    @classmethod
    def find_all(cls) -> list[ProductModel]:
        session = Session()
        products = session.query(ProductModel).all()
        session.close()
        return products

    @classmethod
    def find_by_id(cls, product_id: str) -> ProductModel:
        session = Session()
        product = session.query(ProductModel).filter(ProductModel.id == product_id).first()
        session.close()
        return product

    @classmethod
    def update(cls, product: ProductModel) -> ProductModel:
        session = Session()
        existing = session.query(ProductModel).filter(ProductModel.id == product.id).first()
        if existing:
            existing.name = product.name
            existing.price = product.price
            session.commit()
        session.close()
        return product

    @classmethod
    def delete(cls, product_id: str) -> None:
        session = Session()
        session.query(ProductModel).filter(ProductModel.id == product_id).delete()
        session.commit()
        session.close()

    @classmethod
    def save_all(cls, to_domain_list: list[ProductModel]) -> None:
        session = Session()
        session.add_all(to_domain_list)
        session.commit()
        session.close()
