import unittest

from stream import Riverbed

TEST_VALUES = list(range(100))
TEST_FUNCTION = lambda x: x * 2
TEST_FILTER = lambda x: x % 2 == 0
N_TO_TAKE = 2


class TestRiverbed(unittest.TestCase):
    def test_init(self):
        r = Riverbed()
        self.assertTrue(isinstance(r, Riverbed))

    async def test_init_values(self):
        r = Riverbed(TEST_VALUES)
        for t in TEST_VALUES:
            self.assertEqual(await r.__anext__(), t)

    async def test_through(self):
        r = Riverbed(TEST_VALUES)
        r = r.through(TEST_FUNCTION)
        for t in TEST_VALUES:
            self.assertEqual(await r.__anext__(), TEST_FUNCTION(t))

    async def test_through_2_times(self):
        r = Riverbed(TEST_VALUES)
        r = r.through(TEST_FUNCTION).through(TEST_FUNCTION)
        for t in TEST_VALUES:
            self.assertEqual(await r.__anext__(), TEST_FUNCTION(TEST_FUNCTION(t)))

    async def test_filter(self):
        r = Riverbed(*TEST_VALUES)
        r = r.filter(TEST_FILTER)
        for t in filter(TEST_FILTER, TEST_VALUES):
            self.assertEqual(await r.__anext__(), t)

    async def test_take_length(self):
        r = Riverbed(*TEST_VALUES)
        self.assertEqual(len(await r.take(N_TO_TAKE)), N_TO_TAKE)

    async def test_take_values(self):
        r = Riverbed(*TEST_VALUES)
        values = await r.take(N_TO_TAKE)
        for t1, t2 in zip(values, TEST_VALUES[:N_TO_TAKE]):
            self.assertEqual(t1, t2)

    async def test_take_values_twice(self):
        r = Riverbed(*TEST_VALUES)
        values = await r.take(N_TO_TAKE)
        for t1, t2 in zip(values, TEST_VALUES[:N_TO_TAKE]):
            self.assertEqual(t1, t2)
        values = await r.take(N_TO_TAKE)
        for t1, t2 in zip(values, TEST_VALUES[N_TO_TAKE : N_TO_TAKE * 2]):
            self.assertEqual(t1, t2)

    async def test_fork(self):
        r = Riverbed(*TEST_VALUES)
        r = r.fork(TEST_FILTER, TEST_FUNCTION)
        for t1, t2 in zip(await list(r), TEST_VALUES):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            self.assertEqual(t1, t2)

    async def test_fork_multiple(self):
        r = Riverbed(*TEST_VALUES)
        r = r.fork(
            TEST_FILTER,
            TEST_FUNCTION,
            lambda x: not TEST_FILTER(x),
            lambda x: TEST_FUNCTION(TEST_FUNCTION(x)),
        )
        for t1, t2 in zip(await list(r), TEST_VALUES):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            else:
                t2 = TEST_FUNCTION(TEST_FUNCTION(t2))
            self.assertEqual(t1, t2)


if __name__ == "__main__":
    unittest.main()
