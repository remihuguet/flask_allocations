from typing import List

from allocation.unit_of_work import AbstractUnitOfWork
from allocation.repository import ProductNotFoundException
from allocation.domain_model import Batch, InvalidSkuException, OrderLine, Product


def list_products(uow: AbstractUnitOfWork) -> List[Product]:
    with uow:
        return uow.products.list()


def add_batch(reference: str, sku: str, quantity: int, eta, uow: AbstractUnitOfWork):
    with uow:
        try:
            product = uow.products.get(sku=sku)
        except ProductNotFoundException:
            product = Product(sku=sku, batches=[])
            uow.products.add(product)
        product.batches.append(
            Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)
        )
        uow.products.save(product)
        uow.commit()


def allocate(orderid: str, sku: str, quantity: int, uow: AbstractUnitOfWork) -> str:
    with uow:
        order_line = OrderLine(orderid=orderid, sku=sku, quantity=quantity)
        try:
            product = uow.products.get(sku=sku)
        except ProductNotFoundException:
            raise InvalidSkuException(f"Unknown sku {sku}")
        batch = product.allocate(order_line)
        batchref = batch.reference
        uow.products.save(product)
        uow.commit()
        return batchref
