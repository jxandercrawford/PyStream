from modules.properties.operable import Operable
from typing import Callable
from abc import abstractmethod


class AsyncOperable(Operable):
    """
    An object that has asynchronous and synchronous operations that are chainable.
    """

    @abstractmethod
    def dam(self, action: Callable):
        pass

    @abstractmethod
    def meter(self, time: float):
        pass

