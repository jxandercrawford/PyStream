import asyncio
from modules.utilities.asyncTools import to_async_generator
from typing import AsyncGenerator, AsyncIterator, AsyncIterable


class Confluence(AsyncIterator, AsyncIterable):

    def __init__(self):
        self.__queue = asyncio.Queue()
        self.__active_sources = 0
        self.__gen = None
        self.__gen_ready = asyncio.Event()

    async def __anext__(self):
        if self.__gen is None:
            raise RuntimeWarning("The Confluence must be started in order to be properly consumed.")

        try:
            return await self.__gen.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration

    def __aiter__(self):
        return self

    async def __enqueue(self, items):
        if not isinstance(items, (AsyncGenerator, AsyncIterator, AsyncIterable)):
            items = to_async_generator(items)

        try:
            async for item in items:
                await self.__queue.put(item)
        finally:
            self.__active_sources -= 1
            if self.__active_sources == 0:
                await self.__queue.put(None)

    async def __consume(self):
        await self.__gen_ready.wait()

        try:
            while True:
                item = await self.__queue.get()
                if item is None:
                    break
                yield item
        finally:
            pass

    def feed(self, items):
        asyncio.create_task(self.__enqueue(items))
        self.__active_sources += 1

    def start(self):
        self.__gen = self.__consume()
        self.__gen_ready.set()
