from datetime import date
from typing import List, Optional, Set
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, reference: str, quantity: int, sku: str, eta: Optional[date] = None
    ):
        self.reference = reference
        self.sku = sku
        self.purchased_quantity = quantity
        self.eta = eta
        self._allocated: Set[OrderLine] = set()

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if not self.eta:
            return False
        if not other.eta:
            return True
        return self.eta > other.eta

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line=order_line):
            self._allocated.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocated:
            self._allocated.remove(order_line)

    def can_allocate(self, order_line: OrderLine):
        return (
            order_line.sku == self.sku
            and order_line.quantity <= self.available_quantity
        )

    @property
    def available_quantity(self):
        return self.purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self):
        return sum([o.quantity for o in self._allocated])


class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches

    def allocate(self, order_line: OrderLine) -> Batch:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(order_line))
            batch.allocate(order_line)
            return batch
        except StopIteration:
            raise OutOfStockException()

    def __repr__(self):
        return f"<Product {self.sku}>"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.sku == other.sku

    def __hash__(self):
        return hash(self.sku)

    @property
    def available_quantity(self):
        return sum([b.available_quantity for b in self.batches])


class OutOfStockException(Exception):
    pass


class InvalidSkuException(Exception):
    pass
