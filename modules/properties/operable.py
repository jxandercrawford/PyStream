from abc import abstractmethod


class Operable:
    """
    An object that has operations that are chainable.
    """

    @abstractmethod
    def through(self, action):
        """
        Pass an action onto the data structure.
        """
        pass

    @abstractmethod
    def filter(self, condition):
        """
        Filter the data structure.
        """
        pass

    @abstractmethod
    def fork(self, condition, action, *args):
        """
        Apply actions conditionally within the data structure.
        """
        pass
