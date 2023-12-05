from abc import abstractmethod


class Compilable:
    """
    An object that is able to be compiled.
    """

    @abstractmethod
    def take(self, n):
        pass

    @abstractmethod
    def drain(self):
        pass

    @abstractmethod
    def to_list(self):
        pass
