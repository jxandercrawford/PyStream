#!/usr/bin/env python
"""
File: xio.py
Author: jxandercrawford@gmail.com
Date: 2023-10-6
Purpose: Base classes for building IO processes.
"""

from abc import abstractmethod
import os


class IO:
    """
    Base IO class for passing data.
    """

    @abstractmethod
    def __self__(self):
        pass

    @abstractmethod
    def __validate(self) -> bool:
        """
        Validate that the source exists.
        :returns True if exists and false otherwise.
        """
        pass


class Pull(IO):
    """
    Base Pull class for creating a data source.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __validate(self) -> bool:
        pass

    @abstractmethod
    def pull(self):
        pass


class Push(IO):
    """
    Base Push class for creating a data sink.
    """

    @abstractmethod
    def __init__(self, data):
        pass

    @abstractmethod
    def __validate(self) -> bool:
        pass

    @abstractmethod
    def push(self):
        pass
