from abc import abstractmethod


class Chunkable:
    """
    An object that allows for chunking.
    """

    @abstractmethod
    def chunk(self, n: int):
        pass
