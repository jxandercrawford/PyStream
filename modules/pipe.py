from modules.properties.callableStream import CallableStream
from modules.stream import Stream
from modules.riverbed import Riverbed
from copy import copy


class Pipe(CallableStream):

    def __init__(self):
        self.__xs = lambda x: lambda y: y(*x)

    def __call__(self, *args, asynchronous: bool = False):
        if asynchronous:
            return self.__xs(args)(Riverbed)
        return self.__xs(args)(Stream)

    def through(self, action):
        """
        Append an action to the pipe.
        :param action: An executable action to append to the pipe.
        :return: A Pipe with new action.
        """
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).through(action)
        return dup

    def through_map_on_chunk(self, action):
        """
        Append an action to the process. If items in stream are Chunks then map action to them.
        :param action: An executable action to append to the pipe.
        :return: A Pipe with new action mapped to on Chunks.
        """
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).through_map_on_chunk(action)
        return dup

    def filter(self, condition):
        """
        Filter a stream.
        :param condition: A function that will determine True to pass and False to discard.
        :return: A filtered Pipe.
        """
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).filter(condition)
        return dup

    def chunk(self, n: int):
        """
        Add an accumulator to the pipeline.
        :param int n: Accumulate this many items before passing.
        :return: A Pipe with a new accumulator.
        """
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).chunk(n)
        return dup

    def fork(self, condition, action, *args):
        """
        Will create a branch of the Stream to execute action on by emulating an if, elif, else sequence. A combination
        of filter() and through() where will execute an action if condition is True, else nothing is done.

        This function can accept any number of conditions of actions after the first 2. It will always be parsed as
        (condition1, action1, condition2, action2, . . ., conditionN, actionN). An odd number of arguments sets the
        final argument as the else action.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action: An executable action to append to the pipe if condition is True.
        :returns: A Stream with a new fork.
        """
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).fork(condition, action, *args)
        return dup

    def meter(self, n: float):
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).meter(n)
        return dup

    def dam(self, action):
        dup = copy(self)
        dup.__xs = lambda x: lambda y: self.__xs(x)(y).dam(action)
        return dup