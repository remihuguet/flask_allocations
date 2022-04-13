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


class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches

    def allocate(self, order_line: OrderLine) -> Batch:
        pass

    def __repr__(self):
        return f"<Product {self.sku}>"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.sku == other.sku

    def __hash__(self):
        return hash(self.sku)
