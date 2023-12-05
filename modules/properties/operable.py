from abc import abstractmethod


class Operable:
    """
    An object that has operations that are chainable.
    """

    @abstractmethod
    def through(self, action):
        pass

    @abstractmethod
    def filter(self, condition):
        pass

    @abstractmethod
    def fork(self, condition, action):
        pass
