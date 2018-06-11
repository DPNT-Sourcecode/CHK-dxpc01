from collections import defaultdict
from collections import namedtuple

PriceOffer = namedtuple('PriceOffer', ('quantity', 'price'))
ProductOffer = namedtuple('ProductOffer', ('quantity', 'product'))



PRODUCT_TABLE = {
    'A': {
        'price': 50,
        'offer': [
            PriceOffer(5, 200),
            PriceOffer(3, 130)
        ]
    },
    'B': {
        'price': 30,
        'offer': [PriceOffer(2, 45)]
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
        'offer': [ProductOffer(2, 'B')]
    },
    'F': {
        'price': 10,
        'offer': [ProductOffer(3, 'F')]
    },
}


def get_product(sku):
    product = PRODUCT_TABLE[sku]
    if not product:
        raise ValueError('Product not found' + sku)
    return product


def get_product_discounts(sku, quantity):
    product = get_product(sku)
    discounted_products = defaultdict(int)
    if product['offer'] is not None:
        for offer in product['offer']:
            if isinstance(offer, ProductOffer):
                offer_qty, quantity = quantity // offer.quantity, \
                                      quantity % offer.quantity
                discounted_products[offer.product] = offer_qty
    return discounted_products


def get_price(sku, quantity):
    product = get_product(sku)
    offer_price = 0
    if product['offer'] is not None:
        for offer in product['offer']:
            if isinstance(offer, PriceOffer):
                offer_qty, quantity = quantity // offer.quantity, \
                                      quantity % offer.quantity
                offer_price += offer_qty * offer[1]
    return offer_price + quantity * product['price']


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not isinstance(skus, basestring):
        return -1

    products = defaultdict(int)
    for sku in skus:
        if sku not in PRODUCT_TABLE:
            return -1
        products[sku] += 1

    # Remove discounted products (the related quantity)
    for sku, qty in products.items():
        disc_products = get_product_discounts(sku, qty)
        for disc_sku, qty in disc_products.items():
            products[disc_sku] -= qty

    # Calculate basket
    total = 0
    for sku, qty in products.items():
        if qty >= 0:
            total += get_price(sku, qty)
    return total
