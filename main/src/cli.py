#!/usr/bin/env python
"""
File: xio.py
Author: jxandercrawford@gmail.com
Date: 
Purpose: 
"""
from abc import ABC
from typing import Iterator
from xio import Pull as oPull, Push as oPush


class Pull(oPull, ABC):
    """
    A stdin pull. Will read from stdin until EOF.
    """

    def __init__(self):
        super().__init__()

    def __validate(self) -> bool:
        return True

    def pull(self) -> Iterator:
        """
        Creates and iterator for the pulling of stdin.
        :returns: An iterator.
        """
        while 1:
            try:
                content = input()
            except EOFError:
                break
            except Exception as e:
                raise e

            yield content


class Push(oPush, ABC):
    """
    A stdout push. Will write all output to stdout.
    """

    def __init__(self, data):
        super().__init__(data)
        self.__data = data

    def __validate(self) -> bool:
        return True

    def push(self) -> Iterator:
        """
        Creates and iterator for the push.
        :returns: An iterator.
        """
        for item in self.__data:
            print(item)
            yield item
