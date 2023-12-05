from abc import abstractmethod
from modules.properties.operable import Operable
from modules.properties.chunkable import Chunkable


class OperableChunkable(Operable, Chunkable):
    """
    An object that is operable and chunkable with chunks able to be operated on with through
    """

    @abstractmethod
    def through_map_on_chunk(self, action):
        pass
