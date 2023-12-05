from modules.stream import Stream
from typing import Generator, Iterator, Iterable


def emit(xs: Iterable = None):
    """
    Will create a generator that will repeat itself.
    :param Iterable xs: An iterable to emit with. Defaults to emitting None.
    :return: A generator of the xs iterable that repeats.
    """
    if xs is None:
        xs = [None]

    items = list(xs)
    n = len(items)
    i = 0

    while True:
        yield items[i]
        i += 1

        if i >= n:
            i = 0


class Spring(Stream):

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Generator, Iterator, Iterable)):
            super().__init__(emit(args[0]))
        elif len(args) == 0:
            super().__init__(emit())
        else:
            super().__init__(emit(args))
