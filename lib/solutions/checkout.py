from collections import defaultdict

PRODUCT_TABLE = {
    'A': {
        'price': 50,
        'offer': [(5, 200), (3, 130)]
    },
    'B': {
        'price': 30,
        'offer': [(2, 45)]
    },
    'C': {
        'price': 20,
        'offer': None
    },
    'D': {
        'price': 15,
        'offer': None
    },
    'E': {
        'price': 40,
        'offer': [(2, 'B')]
    },
}


def get_price(sku, quantity):
    product = PRODUCT_TABLE[sku]
    if not product:
        raise ValueError('Product not found' + sku)

    offer_price = 0
    if product['offer'] is not None:
        for offer in product['offer']:
            offer_qty = offer[0]
            offer_qty, quantity = quantity // offer_qty, quantity % offer_qty
            offer_price += offer_qty * offer_price[1]

    if product['offer'] is not None:
        offer_qty = product['offer'][0]
        offer_qty, quantity = quantity // offer_qty, quantity % offer_qty
        offer_price = offer_qty * product['offer'][1]
    else:
        offer_price = 0
    return offer_price + quantity * product['price']


def get_checkout_products(skus):
    # Count the number of same products
    products = defaultdict(int)
    for sku in skus:
        if sku not in PRODUCT_TABLE:
            return -1
        products[sku] += 1
    return products


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not isinstance(skus, basestring):
        return -1

    products = get_checkout_products(skus)

    # Calculate basket
    total = 0
    for sku, qty in products.items():
        total += get_price(sku, qty)
    return total
