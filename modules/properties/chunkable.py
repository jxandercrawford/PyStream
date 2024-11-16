from abc import abstractmethod


class Chunkable:
    """
    An object that allows for chunking.
    """

    @abstractmethod
    def chunk(self, n: int):
        """
        Chunk the data structure into chunks of n.
        """
        pass
