from abc import ABC
from copy import copy
from itertools import chain
from typing import Generator, Iterator, Iterable, Any, Tuple


class Chunk(Tuple):

    def __new__(self, *args):
        return super(Chunk, self).__new__(self, args)

    def __init__(self, *args):
        super().__init__()

    def flat_map(self, f):
        return f(self)

    def map(self, f):
        return Chunk(*map(f, self))


class Stream:

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
        :param action (Executable): An executable action to append to the pipe.
        :return: A Stream with new action.
        """
        if isinstance(action, Pipe):
            return self.flat_map(action)
        return Stream((action(item) for item in self))

    def through_map_on_chunk(self, action):
        """
        Append an action to the process. If items in stream are Chunks then map action to them.
        :param action (Executable): An executable action to append to the pipe.
        :return: A Stream with new action mapped to on Chunks.
        """
        if isinstance(action, Pipe):
            return self.flat_map(action)
        return Stream(item.map(action) if isinstance(item, Chunk) else item for item in self)

    def filter(self, condition):
        """
        Filter a stream.
        :param condition: A function that will determine True to pass and False to discard.
        :return: A filtered Stream.
        """
        return Stream((item for item in self if condition(item)))

    def __chunker(self, n: int) -> Iterator:
        """
        Create an accumulator for source.
        :param n (int): Accumulate this many items before returning.
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
        :param n (int): Accumulate this many items before passing.
        :return: A Stream with a new accumulator.
        """
        return Stream(self.__chunker(n))

    def __forker(self, condition, action):
        """
        Will create a branch of the Stream to execute action on. A combination of filter() and through() where will execute an action if condition is True, else nothing is done.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action (Executable): An executable action to append to the pipe if condition is True.
        :returns: An iterator of the fork.
        """
        for item in self:
            if condition(item) and isinstance(action, Pipe):
                yield next(action(item))
            elif condition(item):
                yield action(item)
            else:
                yield item

    def fork(self, condition, action):
        """
        Will create a branch of the Stream to execute action on. A combination of filter() and through() where will execute an action if condition is True, else nothing is done.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action (Executable): An executable action to append to the pipe if condition is True.
        :returns: A Stream with a new fork.
        """
        return Stream(self.__forker(condition, action))

    def take(self, n: int) -> list[Any]:
        """
        Will compile the process for given amount of iterations. Will return less in event the stream is terminated.
        :param n (int): The number of iterations to compile.
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


class Pipe:

    def __init__(self):
        self.__stream = lambda x: Stream(*x)

    def __call__(self, *args):
        return self.__stream(args)

    def through(self, action):
        """
        Append an action to the pipe.
        :param action (Executable): An executable action to append to the pipe.
        :return: A Pipe with new action.
        """
        dup = copy(self)
        dup.__stream = lambda x: self.__stream(x).through(action)
        return dup

    def through_map_on_chunk(self, action):
        """
        Append an action to the process. If items in stream are Chunks then map action to them.
        :param action (Executable): An executable action to append to the pipe.
        :return: A Pipe with new action mapped to on Chunks.
        """
        dup = copy(self)
        dup.__stream = lambda x: self.__stream(x).through_map_on_chunk(action)
        return dup

    def filter(self, action):
        """
        Filter a stream.
        :param condition: A function that will determine True to pass and False to discard.
        :return: A filtered Pipe.
        """
        dup = copy(self)
        dup.__stream = lambda x: self.__stream(x).filter(action)
        return dup

    def chunk(self, n):
        """
        Add an accumulator to the pipeline.
        :param n (int): Accumulate this many items before passing.
        :return: A Pipe with a new accumulator.
        """
        dup = copy(self)
        dup.__stream = lambda x: self.__stream(x).chunk(n)
        return dup

    def fork(self, condition, action):
        """
        Will create a branch of the Pipe to execute action on. A combination of filter() and through() where will execute an action if condition is True, else nothing is done.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action (Executable): An executable action to append to the pipe if condition is True.
        :returns: A Pipe with a new fork.
        """
        dup = copy(self)
        dup.__stream = lambda x: self.__stream(x).fork(condition, action)
        return dup
