import sqlite3
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


class SQLiteRepository:
    def __init__(self, db_file: str):
        self._db_file = db_file
        self._initialize()

    def _initialize(self):
        self._conn = sqlite3.connect(self._db_file)
        self._cursor = self._conn.cursor()
        try:
            self._cursor.execute("SELECT sku FROM batches")
        except sqlite3.OperationalError:
            self._cursor.execute(
                """CREATE TABLE batches 
            (reference TEXT PRIMARY KEY, sku TEXT NOT NULL, purchased_quantity INTEGER DEFAULT 0, eta TEXT)"""
            )
            self._cursor.execute(
                """CREATE TABLE allocations 
            (orderid TEXT PRIMARY KEY, reference TEXT NOT NULL, quantity INTEGER DEFAULT 0, FOREIGN KEY(reference) REFERENCES batches(reference))"""
            )

            self._commit()

    def save(self, product: Product):
        for batch in product.batches:
            self._cursor.execute(
                "SELECT reference FROM batches WHERE reference=?", (batch.reference,)
            )
            if not self._cursor.fetchone():
                self._cursor.execute(
                    f"INSERT INTO batches VALUES ('{batch.reference}', '{batch.sku}', '{batch.purchased_quantity}', '{batch.eta if batch.eta else ''}') "
                )
            for allocated in batch._allocated:
                try:
                    self._cursor.execute(
                        f"INSERT INTO allocations VALUES ('{allocated.orderid}', '{batch.reference}', '{allocated.quantity}')"
                    )
                except sqlite3.IntegrityError:
                    self._cursor.execute(
                        f"UPDATE allocations SET reference='{batch.reference}', quantity='{allocated.quantity}' WHERE orderid='{allocated.orderid}'"
                    )

        self._commit()

    def _commit(self):
        self._conn.commit()


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
