from modules.properties.operable import Operable
from typing import Callable
from abc import abstractmethod


class AsyncOperable(Operable):

    @abstractmethod
    def dam(self, action: Callable):
        pass

    @abstractmethod
    def meter(self, time: float):
        pass

