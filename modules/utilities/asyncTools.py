import asyncio
from typing import AsyncGenerator, AsyncIterable, Callable, Generator, Iterable


async def to_async_generator(
    items: Iterable, sleep_time: float = 0.0
) -> AsyncGenerator:
    """
    Convert any iterable into an async generator.
    :param items: An iterable to convert.
    :param sleep_time: Add a sleep time between yielding of items in number of seconds.
    :return: An async generator of the given iterable with possible delay time.
    """
    for item in items:
        await asyncio.sleep(sleep_time)
        yield item


async def async_to_async_generator(
    items: AsyncIterable, sleep_time: float = 0.0
) -> AsyncGenerator:
    """
    Convert any async iterable into an async generator.
    :param items: An async iterable to convert.
    :param sleep_time: Add a sleep time between yielding of items in number of seconds.
    :return: An async generator of the given iterable with possible delay time.
    """
    async for item in items:
        await asyncio.sleep(sleep_time)
        yield item


async def amap(action: Callable, items: AsyncIterable) -> AsyncGenerator:
    async for item in items:
        yield action(item)


async def async_amap(action: Callable, items: AsyncIterable) -> AsyncGenerator:
    async for item in items:
        yield await action(item)


async def afilter(condition: Callable, items: AsyncIterable) -> AsyncGenerator:
    async for item in items:
        if condition(item):
            yield item


def async_to_generator(items: AsyncIterable) -> Generator:
    it = items.__aiter__()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def get_next():
        try:
            item = await it.__anext__()
            return False, item
        except StopAsyncIteration:
            return True, None

    while True:
        done, item = loop.run_until_complete(get_next())
        if done:
            break
        yield item
