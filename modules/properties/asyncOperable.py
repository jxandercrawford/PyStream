from abc import abstractmethod
from typing import Callable

from modules.properties.operable import Operable


class AsyncOperable(Operable):
    """
    An object that has asynchronous and synchronous operations that are chainable.
    """

    @abstractmethod
    def dam(self, action: Callable):
        """
        Apply an async callable to the data structure.
        """
        pass

    @abstractmethod
    def meter(self, time: float):
        """
        Block between emitting in the data structure.
        """
        pass
