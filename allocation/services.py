from typing import List
from .domain_model import Product


def list_products() -> List[Product]:
    return [Product(sku="Product 1", batches=[]), Product(sku="Product 2", batches=[])]
