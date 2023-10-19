#!/usr/bin/env python

from xio import Pull
from typing import Iterator
import copy
from abc import abstractmethod


class Hollow:
    def __init__(self):
        pass

    @abstractmethod
    def through(self, action):
        pass


class Pipe(Hollow):

    def __init__(self, *args):
        super().__init__()
        self.__actions = [lambda x: x, *args]

    def __execute(self, *args):
        value = self.__actions[0](*args)
        for action in self.__actions[1:]:
            value = action(value)
        return value

    def through(self, action):
        dup = copy.copy(self)
        dup.__actions.append(action)
        return dup

    def __call__(self, *args):
        return self.__execute(*args)


class Proc(Hollow):

    def __init__(self, source: Iterator):
        super().__init__()
        self.__source = source
        self.__pipe = Pipe()

    def through(self, action):
        """
        Append an action to the process.
        :param action (Executable): A executable action to append to the pipe.
        :returns: A Proc with new action.
        """
        dup = copy.copy(self)
        dup.__pipe.through(action)
        return dup

    def __iter__(self):
        for item in self.__source:
            yield self.__pipe(item)

    def take(self, n: int) -> list:
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


if __name__ == "__main__":
    from cli import Pull as cpull

    proc = Proc(cpull().pull())
    print(proc.through(lambda x: x.upper()).compile())
