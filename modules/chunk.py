from typing import Tuple, Callable


class Chunk(Tuple):

    def __new__(self, *args):
        return super(Chunk, self).__new__(self, args)

    def __init__(self, *args):
        super().__init__()

    def flat_map(self, action: Callable):
        return action(self)

    def map(self, action: Callable):
        """
        Map an action onto the underlying data.
        :param action: A callable to evaluate on each item.
        :return: A Chunk with the data evaluated by the action.
        """
        return Chunk(*map(action, self))
