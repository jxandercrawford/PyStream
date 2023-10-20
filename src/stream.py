#!/usr/bin/env python
"""
File: stream.py
Author: jxandercrawford@gmail.com
Date: 2023-10-18
Purpose: Stream & Pipe classes for building generator based pipelines.
"""

from typing import Iterator, Any
import copy
from abc import abstractmethod


class Hollow:
    def __init__(self):
        pass

    @abstractmethod
    def through(self, action):
        pass


class Pipe(Hollow):
    """
    An sequence of actions to be run on a given input.
    """

    def __init__(self, *args):
        super().__init__()
        self.__actions = [lambda x: x, *args]

    def __call__(self, *args):
        return self.__execute(*args)

    def __execute(self, *args):
        value = self.__actions[0](*args)
        for action in self.__actions[1:]:
            value = action(value)
        return value

    def through(self, action):
        dup = copy.copy(self)
        dup.__actions.append(action)
        return dup


class Stream(Hollow):
    """
    An extendable iterator with a builtin Pipe to process items with.
    """

    def __init__(self, source: Iterator):
        super().__init__()
        self.__source = source
        self.__pipe = Pipe()

    def __iter__(self):
        for item in self.__source:
            yield self.__pipe(item)

    def through(self, action):
        """
        Append an action to the process.
        :param action (Executable): An executable action to append to the pipe.
        :returns: A Stream with new action.
        """
        dup = copy.copy(self)
        dup.__pipe.through(action)
        return dup

    def filter(self, condition):
        """
        Filter a stream.
        :param condition: A function that will determine True to pass and False to discard.
        :returns: A filtered Stream.
        """
        return Stream((x for x in self if condition(x)))

    def __chunker(self, n: int) -> Iterator:
        """
        Create an accumulator for source.
        :param n (int): Accumulate this many items before returning.
        :returns: An iterator of chunks.
        """
        acc = []
        cnt = 0

        for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                yield acc
                cnt = 0
                acc = []
        yield acc

    def chunk(self, n: int):
        """
        Add an accumulator to the pipeline.
        :param n (int): Accumulate this many items before passing.
        :returns: A Stream with a new accumulator.
        """
        return Stream(self.__chunker(n))

    def take(self, n: int) -> list[Any]:
        """
        Will compile the process for given amount of iterations. Will return less in event the stream is terminated.
        :param n (int): The number of iterations to compile.
        :returns: A list containing pipe output.
        """
        acc = []
        cnt = 0

        for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                break
        return acc

    def compile(self) -> list:
        """
        Compiles the process.
        :returns: A list containing pipe output.
        """
        return list(self)

    def drain(self):
        """
        Compiles the process and drains output.
        :returns: None.
        """
        self.compile()
