import sqlite3
from typing import Protocol
from allocation.domain_model import Batch, OrderLine, Product


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
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._initialize()

    def _initialize(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT sku FROM batches")
        except sqlite3.OperationalError:
            cursor.execute(
                """CREATE TABLE batches
            (reference TEXT PRIMARY KEY, sku TEXT NOT NULL, purchased_quantity INTEGER DEFAULT 0, eta TEXT)"""
            )
            cursor.execute(
                """CREATE TABLE allocations
            (orderid TEXT PRIMARY KEY, reference TEXT NOT NULL,
            quantity INTEGER DEFAULT 0, FOREIGN KEY(reference) REFERENCES batches(reference))"""
            )
            self._conn.commit()

    def save(self, product: Product):
        cursor = self._conn.cursor()
        for batch in product.batches:
            cursor.execute(
                "SELECT reference FROM batches WHERE reference=?", (batch.reference,)
            )
            if not cursor.fetchone():
                cursor.execute(
                    f"""INSERT INTO batches
                    VALUES
                    ('{batch.reference}', '{batch.sku}', '{batch.purchased_quantity}',
                    '{batch.eta if batch.eta else ''}')"""
                )
            for allocated in batch._allocated:
                try:
                    cursor.execute(
                        f"""INSERT INTO allocations
                        VALUES ('{allocated.orderid}', '{batch.reference}', '{allocated.quantity}')"""
                    )
                except sqlite3.IntegrityError:
                    cursor.execute(
                        f"""UPDATE allocations SET reference='{batch.reference}', quantity='{allocated.quantity}'
                         WHERE orderid='{allocated.orderid}'"""
                    )

    def add(self, product: Product):
        self.save(product)

    def get(self, sku: str) -> Product:
        cursor = self._conn.cursor()
        cursor.execute(
            f"""SELECT * FROM batches LEFT JOIN allocations ON batches.reference = allocations.reference
            WHERE batches.sku='{sku}'"""
        )

        batches = SQLiteRepository._to_batches(cursor.fetchall())
        if not batches:
            raise ProductNotFoundException()
        return Product(sku=sku, batches=list(batches))

    @staticmethod
    def _to_batches(results) -> list[Batch]:
        batches = set()
        for res in results:
            try:
                batch = next(b for b in batches if b.reference == res[0])
            except StopIteration:
                batch = Batch(
                    reference=res[0],
                    quantity=res[2],
                    sku=res[1],
                    eta=res[3],
                )
                batches.add(batch)
            if res[4]:
                batch._allocated.add(
                    OrderLine(orderid=res[4], sku=res[1], quantity=res[6])
                )
        return batches

    def list(self) -> list[Product]:
        cursor = self._conn.cursor()
        cursor.execute(
            """SELECT * FROM batches LEFT JOIN allocations ON batches.reference = allocations.reference"""
        )
        batches = SQLiteRepository._to_batches(cursor.fetchall())
        products = list()

        for batch in batches:
            try:
                product = next(p for p in products if p.sku == batch.sku)
            except StopIteration:
                product = Product(sku=batch.sku, batches=[])
                products.append(product)
            product.batches.append(batch)
        return products


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
