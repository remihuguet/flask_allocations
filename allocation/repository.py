from typing import Protocol
from allocation.domain_model import Product


class ProductNotFoundException(Exception):
    pass


class Repository(Protocol):
    def get(self, sku: str) -> Product:
        pass

    def add(self, product: Product):
        pass

    def list(self) -> list[Product]:
        pass

    def save(self, product: Product):
        pass


class InMemoryRepository:
    def __init__(self, products: list[Product]):
        self._products = set(products)

    def get(self, sku: str) -> Product:
        try:
            return next(filter(lambda p: p.sku == sku, self._products))
        except StopIteration:
            raise ProductNotFoundException(f"Product with sku {sku} not found")

    def add(self, product: Product):
        self._products.add(product)

    def list(self) -> list[Product]:
        return list(self._products)

    def save(self, product: Product):
        self._products.discard(product)
        self._products.add(product)


def initialize_repository(repo_class):
    if repo_class == "InMemoryRepository":
        return InMemoryRepository(products=[])
