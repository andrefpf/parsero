def consume(iterator, n):
    for i in range(n):
        try:
            next(iterator)
        except StopIteration:
            return