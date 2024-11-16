from abc import abstractmethod

from modules.properties.chunkable import Chunkable
from modules.properties.operable import Operable


class OperableChunkable(Operable, Chunkable):
    """
    An object that is operable and chunkable with chunks able to be operated on with through
    """

    @abstractmethod
    def through_map_on_chunk(self, action):
        """
        Map a callable onto a chunk within the data structure.
        """
        pass
