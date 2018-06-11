# noinspection PyShadowingBuiltins,PyUnusedLocal
def sum(x, y):
    if not (0 <= x <= 100 and 0 <= y <= 100):
        raise ValueError('Invalid arguments: {}, {}. A positive integer '
                         'between [0, 100] is expected.'.format(x, y))
    return x + y

