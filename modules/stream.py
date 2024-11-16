from itertools import chain
from typing import Generator, Iterable, Iterator

from modules.chunk import Chunk
from modules.properties.callableStream import CallableStream
from modules.properties.compilable import Compilable
from modules.properties.operableChunkable import OperableChunkable


class Stream(OperableChunkable, Compilable):
    """
    An immutable streaming datatype.
    """

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Generator, Iterator, Iterable)):
            self.__items = (i for i in args[0])
        else:
            self.__items = (i for i in args)

    def __next__(self):
        return next(self.__items)

    def __iter__(self):
        for item in self.__items:
            yield item

    def __add__(self, other):
        return Stream(chain(self, other))

    def flat_map(self, action):
        return action(self.__items)

    def through(self, action):
        """
        Append an action to the process.
        :param action: An executable action to append to the pipe.
        :return: A Stream with new action.
        """
        if isinstance(action, CallableStream):
            return self.flat_map(action)
        return Stream((action(item) for item in self))

    def through_map_on_chunk(self, action):
        """
        Append an action to the process. If items in stream are Chunks then map action to them.
        :param action: An executable action to append to the pipe.
        :return: A Stream with new action mapped to on Chunks.
        """
        if isinstance(action, CallableStream):
            return self.flat_map(action)
        return Stream(
            item.map(action) if isinstance(item, Chunk) else item for item in self
        )

    def filter(self, condition):
        """
        Filter a stream.
        :param condition: A function that will determine True to pass and False to discard.
        :return: A filtered Stream.
        """
        return Stream((item for item in self if condition(item)))

    def __chunker(self, n: int):
        """
        Create an accumulator for source.
        :param int n: Accumulate this many items before returning.
        :return: An iterator of chunks.
        """
        acc = []
        cnt = 0

        for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                yield Chunk(*acc)
                cnt = 0
                acc = []
        yield Chunk(*acc)

    def chunk(self, n: int):
        """
        Add an accumulator to the pipeline.
        :param int n: Accumulate this many items before passing.
        :return: A Stream with a new accumulator.
        """
        return Stream(self.__chunker(n))

    def __forker(self, condition, action, *args):
        """
        Will create a branch of the Stream to execute action on by emulating an if, elif, else sequence. A combination
        of filter() and through() where will execute an action if condition is True, else nothing is done.

        This function can accept any number of conditions of actions after the first 2. It will always be parsed as
        (condition1, action1, condition2, action2, . . ., conditionN, actionN). An odd number of arguments sets the
        final argument as the else action.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action: An executable action to append to the pipe if condition is True.
        :returns: An iterator of a fork.
        """
        prongs = [condition, action, *args]

        for item in self:
            yielded = False

            # Run loop to simulate if, elif, else
            for i in range(0, len(prongs), 2):

                # Catch if single last argument for else statement
                if i == len(prongs) - 1:
                    condition = lambda x: True
                    action = prongs[i]
                else:
                    condition = prongs[i]
                    action = prongs[i + 1]

                if condition(item) and isinstance(action, CallableStream):
                    yield next(action(item))
                    yielded = True
                    break
                elif condition(item):
                    yield action(item)
                    yielded = True
                    break
            # If condition never satisfied yield item unchanged
            if not yielded:
                yield item

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
        return Stream(self.__forker(condition, action, *args))

    def take(self, n: int) -> list:
        """
        Will compile the process for given amount of iterations. Will return less in event the stream is terminated.
        :param int n: The number of iterations to compile.
        :return: A list containing pipe output.
        """
        acc = []
        cnt = 0

        for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                break
        return acc

    def to_list(self):
        """
        Compiles the stream to a list.
        :return: A list containing pipe output.
        """
        return list(self.__items)

    def drain(self):
        """
        Complies a stream and drains output for each item.
        :return: None
        """
        for _ in self.__items:
            pass
