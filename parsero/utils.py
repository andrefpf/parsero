def consume(n, iterator):
    """
    Ignore the next n values of an iterator.
    """
    for i in range(n):
        try:
            next(iterator)
        except StopIteration:
            return
