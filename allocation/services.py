from typing import List

from allocation.repository import ProductNotFoundException, Repository
from allocation.domain_model import Batch, InvalidSkuException, OrderLine, Product


def list_products(repository: Repository) -> List[Product]:
    return repository.list()


def add_batch(reference: str, sku: str, quantity: int, eta, repository: Repository):
    try:
        product = repository.get(sku=sku)
    except ProductNotFoundException:
        product = Product(sku=sku, batches=[])
        repository.add(product)
    product.batches.append(
        Batch(reference=reference, sku=sku, quantity=quantity, eta=eta)
    )
    repository.save(product)


def allocate(orderid: str, sku: str, quantity: int, repository: Repository) -> str:
    order_line = OrderLine(orderid=orderid, sku=sku, quantity=quantity)
    try:
        product = repository.get(sku=sku)
    except ProductNotFoundException:
        raise InvalidSkuException(f"Unknown sku {sku}")
    batch = product.allocate(order_line)
    batchref = batch.reference
    repository.save(product)
    return batchref
