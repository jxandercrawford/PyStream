from abc import abstractmethod
from modules.properties.operable import Operable


class CallableStream(Operable):
    """
    An object that when called will produce a Stream.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
