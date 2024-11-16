from abc import abstractmethod


class Compilable:
    """
    An object that is able to be compiled.
    """

    @abstractmethod
    def take(self, n):
        """
        Return n items from the data structure with effect.
        """
        pass

    @abstractmethod
    def drain(self):
        """
        Exhaust the data structure completely.
        """
        pass

    @abstractmethod
    def to_list(self):
        """
        Convert the data structure to a list.
        """
        pass
