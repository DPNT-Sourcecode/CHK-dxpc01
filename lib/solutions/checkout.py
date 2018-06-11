from collections import defaultdict
from collections import namedtuple

PriceOffer = namedtuple('PriceOffer', ('quantity', 'price'))
ProductOffer = namedtuple('ProductOffer', ('quantity', 'product'))
SpecialOffer = namedtuple('SpecialOffer', ('group_id',))
GroupDiscount = namedtuple('GroupDiscount', ('skus', 'quantity', 'price'))

PRODUCT_TABLE = {
    'A': {'price': 50, 'offer': [PriceOffer(5, 200), PriceOffer(3, 130)]},
    'B': {'price': 30, 'offer': [PriceOffer(2, 45)]},
    'C': {'price': 20},
    'D': {'price': 15},
    'E': {'price': 40, 'offer': [ProductOffer(2, 'B')]},
    'F': {'price': 10, 'offer': [ProductOffer(3, 'F')]},
    'G': {'price': 20},
    'H': {'price': 10, 'offer': [PriceOffer(10, 80), PriceOffer(5, 45)]},
    'I': {'price': 35},
    'J': {'price': 60},
    'K': {'price': 80, 'offer': [PriceOffer(2, 150)]},
    'L': {'price': 90},
    'M': {'price': 15},
    'N': {'price': 40, 'offer': [ProductOffer(3, 'M')]},
    'O': {'price': 10},
    'P': {'price': 50, 'offer': [PriceOffer(5, 200)]},
    'Q': {'price': 30, 'offer': [PriceOffer(3, 80)]},
    'R': {'price': 50, 'offer': [ProductOffer(3, 'Q')]},
    'S': {'price': 20, 'offer': [SpecialOffer(1)]},
    'T': {'price': 20, 'offer': [SpecialOffer(1)]},
    'U': {'price': 40, 'offer': [ProductOffer(4, 'U')]},
    'V': {'price': 50, 'offer': [PriceOffer(3, 130), PriceOffer(2, 90)]},
    'W': {'price': 20},
    'X': {'price': 17, 'offer': [SpecialOffer(1)]},
    'Y': {'price': 20, 'offer': [SpecialOffer(1)]},
    'Z': {'price': 21, 'offer': [SpecialOffer(1)]},
}

GROUP_DISCOUNTS = {
    1: GroupDiscount({'S', 'T', 'X', 'Y', 'Z'}, 3, 45)
}


def get_product(sku):
    product = PRODUCT_TABLE[sku]
    if not product:
        raise ValueError('Product not found' + sku)
    return product


def get_other_product_discounts(sku, quantity):
    product = get_product(sku)
    discounted_products = defaultdict(int)
    # The product offer should be sorted by quantity descending
    if 'offer' in product:
        for offer in product['offer']:
            if isinstance(offer, ProductOffer):
                offer_qty, quantity = quantity // offer.quantity, \
                                      quantity % offer.quantity
                discounted_products[offer.product] = offer_qty
    return discounted_products


def get_price(sku, quantity):
    product = get_product(sku)
    offer_price = 0
    if 'offer' in product:
        for offer in product['offer']:
            if isinstance(offer, PriceOffer):
                offer_qty, quantity = quantity // offer.quantity, \
                                      quantity % offer.quantity
                offer_price += offer_qty * offer[1]
    return offer_price + quantity * product['price']


def process_group_discounts_price(products):
    groups = defaultdict(int)
    group_skus = defaultdict(list)

    # Aggregate all products that are part pf a specific group offer
    for sku, qty in products.items():
        product = get_product(sku)
        if 'offer' not in product:
            continue

        for offer in product['offer']:
            if not isinstance(offer, SpecialOffer):
                continue
            group = GROUP_DISCOUNTS[offer.group_id]
            if sku in group.skus:
                groups[offer.group_id] += qty
                group_skus[offer.group_id].append(sku)

    # Apply the group discounts to all products
    special_price = 0
    for group_id, group_qty in groups.items():
        group = GROUP_DISCOUNTS[group_id]
        discounted_count = (group_qty // group.quantity) * group.quantity
        special_price += (group_qty // group.quantity) * group.price

        while discounted_count > 0:
            for sku in group_skus[group_id]:
                discounted = min(discounted_count, products[sku])
                discounted_count -= discounted
                products[sku] -= discounted

    return special_price


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

    total = process_group_discounts_price(products)

    # Remove discounted products (the related quantity)
    for sku, qty in products.items():
        disc_products = get_other_product_discounts(sku, qty)
        for disc_sku, qty in disc_products.items():
            products[disc_sku] -= qty

    # Calculate basket
    for sku, qty in products.items():
        if qty > 0:
            total += get_price(sku, qty)

    return total
