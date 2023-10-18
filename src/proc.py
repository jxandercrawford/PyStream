#!/usr/bin/env python

from xio import Pull
import copy


class Proc():

    def __init__(self, source: Pull):
        self.__source = source.pull()
        self.__pipe = []

    def __build_pipe(self, data):
        acc = data
        for func in self.__pipe:
            acc = func(acc)
        return acc

    def map(self, func):
        new = copy.copy(self)
        new.__pipe.append(func)
        return new

    def __iter__(self):
        for item in self.__source:
            yield self.__build_pipe(item)
