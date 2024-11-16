from typing import (AsyncGenerator, AsyncIterable, AsyncIterator, Callable,
                    Generator, Iterable, Iterator)

from modules.properties.asyncOperable import AsyncOperable
from modules.properties.callableStream import CallableStream
from modules.utilities.asyncTools import (afilter, amap, async_amap,
                                          async_to_async_generator,
                                          to_async_generator)


class Riverbed(AsyncOperable):
    """
    An asynchronous Stream.
    """

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Generator, Iterator, Iterable)):
            self.__items = to_async_generator(args[0])
        elif len(args) == 1 and isinstance(
            args[0], (AsyncGenerator, AsyncIterator, AsyncIterable)
        ):
            self.__items = async_to_async_generator(args[0])
        else:
            self.__items = to_async_generator((i for i in args))

    async def __anext__(self):
        try:
            return await self.__items.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration

    def __aiter__(self):
        return self

    def flat_map(self, action: Callable):
        return action(self.__items)

    def through(self, action: Callable):
        """
        Append an action to the process.
        :param action: An executable action to append to the pipe.
        :return: A Riverbed with new action.
        """
        if isinstance(action, CallableStream):
            return self.flat_map(lambda x: action(x, asynchronous=True))
        return Riverbed(amap(action, self))

    def filter(self, condition: Callable):
        """
        Filter a riverbed.
        :param condition: A function that will determine True to pass and False to discard.
        :return: A filtered Riverbed.
        """
        return Riverbed(afilter(condition, self))

    async def __forker(self, condition: Callable, action: Callable, *args):
        """
        Will create a branch of the Riverbed to execute action on by emulating an if, elif, else sequence. A combination
        of filter() and through() where will execute an action if condition is True, else nothing is done.

        This function can accept any number of conditions of actions after the first 2. It will always be parsed as
        (condition1, action1, condition2, action2, . . ., conditionN, actionN). An odd number of arguments sets the
        final argument as the else action.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action: An executable action to append to the pipe if condition is True.
        :returns: An iterator of a fork.
        """
        prongs = [condition, action, *args]

        async for item in self:
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

                if condition(item):
                    yield action(item)
                    yielded = True
                    break
            # If condition never satisfied yield item unchanged
            if not yielded:
                yield item

    def fork(self, condition, action, *args):
        """
        Will create a branch of the Riverbed to execute action on by emulating an if, elif, else sequence. A combination
        of filter() and through() where will execute an action if condition is True, else nothing is done.

        This function can accept any number of conditions of actions after the first 2. It will always be parsed as
        (condition1, action1, condition2, action2, . . ., conditionN, actionN). An odd number of arguments sets the
        final argument as the else action.
        :param condition: A function that will determine True to pass to action and False to skip.
        :param action: An executable action to append to the pipe if condition is True.
        :returns: A Riverbed with a new fork.
        """
        return Riverbed(self.__forker(condition, action, *args))

    def dam(self, action: Callable):
        """
        Append an asynchronous action to the process.
        :param action: An asynchronous executable action to append to the pipe.
        :return: A Riverbed with new action.
        """
        return Riverbed(async_amap(action, self))

    def meter(self, time: float):
        """
        Put sleep time into the pipeline before yielding to the next operation.
        :param time: The amount of time to sleep in seconds.
        :return: A Riverbed with a delay.
        """
        return Riverbed(async_to_async_generator(self, time))

    async def take(self, n: int):
        """
        Will compile the process for given amount of iterations. Will return less in event the Riverbed is terminated.
        :param int n: The number of iterations to compile.
        :return: A list containing pipe output.
        """
        acc = []
        cnt = 0

        async for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                break
        return acc
