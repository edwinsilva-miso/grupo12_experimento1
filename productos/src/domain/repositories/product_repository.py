from abc import ABC, abstractmethod
from ..entities.product_dto import ProductDTO

class ProductDTORepository(ABC):
    @abstractmethod
    def get_all(self) -> list[ProductDTO]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> ProductDTO:
        pass

    @abstractmethod
    def add(self, product: ProductDTO) -> str:
        pass

    @abstractmethod
    def update(self, product: ProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass