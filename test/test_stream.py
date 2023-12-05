import unittest
from stream import Stream
from typing import Iterator

TEST_VALUES = list(range(100))
TEST_FUNCTION = lambda x: x * 2
TEST_FILTER = lambda x: x % 2 == 0
N_TO_TAKE = 2


class TestStream(unittest.TestCase):
    def test_init(self):
        s = Stream()
        self.assertTrue(isinstance(s, Stream))

    def test_iterator(self):
        s = Stream()
        self.assertTrue(isinstance(s, Iterator))

    # Need to implement coroutines functionality
    # def test_generator(self):
    #     s = Stream()
    #     self.assertTrue(isinstance(s, Generator))

    def test_accept_values(self):
        s = Stream(*TEST_VALUES)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, t2)

    def test_addition(self):
        s = Stream(*TEST_VALUES) + Stream(*TEST_VALUES)
        for t1, t2 in zip(s, [*TEST_VALUES, *TEST_VALUES]):
            self.assertEqual(t1, t2)

    def test_flat_map(self):
        s = Stream(*TEST_VALUES)
        s = s.flat_map(lambda x: Stream(x).through(TEST_FUNCTION))
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(t2))

    def test_through(self):
        s = Stream(*TEST_VALUES)
        s = s.through(TEST_FUNCTION)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(t2))

    def test_through_2_times(self):
        s = Stream(*TEST_VALUES)
        s = s.through(TEST_FUNCTION).through(TEST_FUNCTION)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(TEST_FUNCTION(t2)))

    def test_filter(self):
        s = Stream(*TEST_VALUES)
        s = s.filter(TEST_FILTER)
        for t1, t2 in zip(s, (i for i in TEST_VALUES if TEST_FILTER(i))):
            self.assertEqual(t1, t2)

    def test_take_length(self):
        s = Stream(*TEST_VALUES)
        self.assertEqual(len(s.take(N_TO_TAKE)), N_TO_TAKE)

    def test_take_values(self):
        s = Stream(*TEST_VALUES)
        for t1, t2 in zip(s.take(N_TO_TAKE), TEST_VALUES[:N_TO_TAKE]):
            self.assertEqual(t1, t2)

    def test_take_values_twice(self):
        s = Stream(*TEST_VALUES)
        for t1, t2 in zip(s.take(N_TO_TAKE), TEST_VALUES[:N_TO_TAKE]):
            self.assertEqual(t1, t2)
        for t1, t2 in zip(s.take(N_TO_TAKE), TEST_VALUES[N_TO_TAKE:N_TO_TAKE+N_TO_TAKE]):
            self.assertEqual(t1, t2)

    def test_chunking_length(self):
        s = Stream(*TEST_VALUES).chunk(N_TO_TAKE)
        self.assertEqual(len(next(s)), N_TO_TAKE)

    def test_chunking_values(self):
        s = Stream(*TEST_VALUES).chunk(N_TO_TAKE)
        self.assertEqual(next(s), tuple(TEST_VALUES[:N_TO_TAKE]))

    def test_chunking_values_twice(self):
        s = Stream(*TEST_VALUES).chunk(N_TO_TAKE)
        self.assertEqual(next(s), tuple(TEST_VALUES[:N_TO_TAKE]))
        self.assertEqual(next(s), tuple(TEST_VALUES[N_TO_TAKE:N_TO_TAKE*2]))

    def test_map_on_chunk(self):
        s = Stream(*TEST_VALUES).chunk(N_TO_TAKE).through_map_on_chunk(TEST_FUNCTION)
        self.assertEqual(next(s), tuple(map(TEST_FUNCTION, TEST_VALUES[:N_TO_TAKE])))
        self.assertEqual(next(s), tuple(map(TEST_FUNCTION, TEST_VALUES[N_TO_TAKE:N_TO_TAKE*2])))

    def test_to_list(self):
        s = Stream(*TEST_VALUES)
        self.assertEqual(s.to_list(), list(TEST_VALUES))

    def test_fork(self):
        s = Stream(*TEST_VALUES)
        s = s.fork(TEST_FILTER, TEST_FUNCTION)
        for t1, t2 in zip(s, TEST_VALUES):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            self.assertEqual(t1, t2)

    def test_fork_multiple(self):
        s = Stream(*TEST_VALUES)
        s = s.fork(TEST_FILTER, TEST_FUNCTION, lambda x: not TEST_FILTER(x), lambda x: TEST_FUNCTION(TEST_FUNCTION(x)))
        for t1, t2 in zip(s, list(TEST_VALUES)):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            else:
                t2 = TEST_FUNCTION(TEST_FUNCTION(t2))
            self.assertEqual(t1, t2)


if __name__ == '__main__':
    unittest.main()
