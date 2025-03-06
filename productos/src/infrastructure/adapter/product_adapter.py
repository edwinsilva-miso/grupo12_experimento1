from ...domain.entities.product_dto import ProductDTO
from ...domain.repositories.product_repository import ProductDTORepository
from ..dao.product_dao import ProductDAO
from ..mapper.product_mapper import ProductMapper


class ProductAdapter(ProductDTORepository):

    def get_all(self) -> list[ProductDTO]:
        return ProductMapper.to_dto_list(ProductDAO.find_all())

    def get_by_id(self, id: str) -> ProductDTO:
        return ProductMapper.to_dto(ProductDAO.find_by_id(id))

    def add(self, product: ProductDTO) -> str:
        return ProductDAO.save(ProductMapper.to_domain(product))

    def save_all(self, products: list[ProductDTO]) -> None:
        ProductDAO.save_all(ProductMapper.to_domain_list(products))

    def update(self, product: ProductDTO) -> ProductDTO:
        return ProductMapper.to_dto(ProductDAO.update(ProductMapper.to_domain(product)))

    def delete(self, id: str) -> None:
        ProductDAO.delete(id)
