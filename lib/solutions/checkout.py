from collections import defaultdict

PRODUCT_TABLE = {
    'A': {
        'price': 50,
        'offer': (3, 130)
    },
    'B': {
        'price': 30,
        'offer': (2, 45)
    },
    'C': {
        'price': 20,
        'offer': None
    },
    'D': {
        'price': 15,
        'offer': None
    },
}


def get_price(sku, quantity):
    product = PRODUCT_TABLE[sku]
    if not product:
        raise ValueError('Product not found' + sku)
    if product['offer'] is not None:
        offer_qty = product['offer'][0]
        offer_qty, quantity = quantity // offer_qty, quantity % offer_qty
        offer_price = offer_qty * product['offer'][1]
    else:
        offer_price = 0
    return offer_price + quantity * product['price']


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not isinstance(skus, str):
        return -1

    # Count the number of same products
    products = defaultdict(int)
    for sku in skus:
        if sku not in PRODUCT_TABLE:
            return -1
        products[sku] += 1

    # Calculate basket
    total = 0
    for sku, qty in products.items():
        total += get_price(sku, qty)
    return total
