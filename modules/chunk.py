from typing import Tuple


class Chunk(Tuple):

    def __new__(self, *args):
        return super(Chunk, self).__new__(self, args)

    def __init__(self, *args):
        super().__init__()

    def flat_map(self, f):
        return f(self)

    def map(self, f):
        return Chunk(*map(f, self))
