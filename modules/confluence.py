import asyncio
from modules.utilities.asyncTools import to_async_generator
from typing import Iterable, AsyncIterator, AsyncIterable, Union


class Confluence(AsyncIterator):

    def __init__(self):
        self.__queue = asyncio.Queue()
        self.__active_sources = 0
        self.__gen = None
        self.__gen_ready = asyncio.Event()

    async def __anext__(self):
        if not self.__gen_ready.is_set():
            raise RuntimeWarning("The Confluence must be started via `start()` in order to be properly consumed.")

        try:
            return await self.__gen.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration

    def __aiter__(self):
        return self

    async def __enqueue(self, items: Union[Iterable, AsyncIterable]):
        """
        Enqueue an item to the underlying asyncio Queue object.
        :param items: The source to enqueue.
        :return: None.
        """
        if not isinstance(items, AsyncIterable):
            items = to_async_generator(items)

        try:
            async for item in items:
                await self.__queue.put(item)
        finally:
            self.__active_sources -= 1
            if self.__active_sources == 0:
                await self.__queue.put(None)

    async def __consume(self):
        """
        Consume the items in the queue by creating an AsyncGenerator.
        :return: None.
        """
        await self.__gen_ready.wait()

        try:
            while True:
                item = await self.__queue.get()
                if item is None:
                    break
                yield item
        finally:
            pass

    def feed(self, items: Union[Iterable, AsyncIterable]):
        """
        Add a source to be fed into the queue for evaluation asynchronously.
        :param items: The items to be fed to the queue.
        :return: None.
        """
        asyncio.create_task(self.__enqueue(items))
        self.__active_sources += 1

    def start(self):
        """
        Start the evaluation of the queue. Required to iterate over the items.
        :return: None.
        """
        self.__gen = self.__consume()
        self.__gen_ready.set()
