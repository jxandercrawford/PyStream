from typing import Callable, Generator, Iterator, Iterable, AsyncGenerator, AsyncIterator, AsyncIterable
from modules.utilities.asyncTools import to_async_generator, async_to_async_generator, amap, afilter, async_amap
from modules.properties.asyncOperable import AsyncOperable


class Riverbed(AsyncOperable):

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Generator, Iterator, Iterable)):
            self.__items = to_async_generator(args[0])
        elif len(args) == 1 and isinstance(args[0], (AsyncGenerator, AsyncIterator, AsyncIterable)):
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

    def through(self, action: Callable):
        return Riverbed(amap(action, self))

    def filter(self, condition: Callable):
        return Riverbed(afilter(condition, self))

    async def __forker(self, condition: Callable, action: Callable, *args):
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
        return Riverbed(self.__forker(condition, action, *args))

    def dam(self, action: Callable):
        return Riverbed(async_amap(action, self))

    def meter(self, time: float):
        return Riverbed(async_to_async_generator(self, time))

    async def take(self, n: int):
        acc = []
        cnt = 0

        async for item in self:
            acc.append(item)
            cnt += 1
            if cnt >= n:
                break
        return acc
