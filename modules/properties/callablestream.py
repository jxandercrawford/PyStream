from abc import abstractmethod
from modules.properties.operablechunkable import OperableChunkable


class CallableStream(OperableChunkable):
    """
    An object that when called will produce a Stream.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
