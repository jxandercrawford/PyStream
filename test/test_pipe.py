import unittest

from stream import Stream, Pipe

TEST_VALUES = range(100)
TEST_FUNCTION = lambda x: x * 2
TEST_FILTER = lambda x: x % 2 == 0
N_TO_TAKE = 2


class TestPipe(unittest.TestCase):
    def test_init(self):
        p = Pipe()
        self.assertTrue(isinstance(p, Pipe))

    def test_identity(self):
        p = Pipe()
        s = Stream(*TEST_VALUES).through(p)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, t2)

    def test_through(self):
        p = Pipe().through(TEST_FUNCTION)
        s = Stream(*TEST_VALUES).through(p)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(t2))

    def test_through_2_times(self):
        p = Pipe().through(TEST_FUNCTION).through(TEST_FUNCTION)
        s = Stream(*TEST_VALUES).through(p)
        for t1, t2 in zip(s, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(TEST_FUNCTION(t2)))

    def test_filter(self):
        p = Pipe().filter(TEST_FILTER)
        s = Stream(*TEST_VALUES).through(p)
        for t1, t2 in zip(s, (i for i in TEST_VALUES if TEST_FILTER(i))):
            self.assertEqual(t1, t2)

    def test_chunking_length(self):
        p = Pipe().chunk(N_TO_TAKE)
        s = Stream(*TEST_VALUES).through(p)
        self.assertEqual(len(next(s)), N_TO_TAKE)

    def test_chunking_values(self):
        p = Pipe().chunk(N_TO_TAKE)
        s = Stream(*TEST_VALUES).through(p)
        self.assertEqual(next(s), tuple(TEST_VALUES[:N_TO_TAKE]))

    def test_chunking_values_twice(self):
        p = Pipe().chunk(N_TO_TAKE)
        s = Stream(*TEST_VALUES).through(p)
        self.assertEqual(next(s), tuple(TEST_VALUES[:N_TO_TAKE]))
        self.assertEqual(next(s), tuple(TEST_VALUES[N_TO_TAKE:N_TO_TAKE*2]))

    def test_map_on_chunk(self):
        p = Pipe().chunk(N_TO_TAKE).through_map_on_chunk(TEST_FUNCTION)
        s = Stream(*TEST_VALUES).through(p)
        self.assertEqual(next(s), tuple(map(TEST_FUNCTION, TEST_VALUES[:N_TO_TAKE])))
        self.assertEqual(next(s), tuple(map(TEST_FUNCTION, TEST_VALUES[N_TO_TAKE:N_TO_TAKE*2])))

    def test_fork(self):
        p = Pipe().fork(TEST_FILTER, TEST_FUNCTION)
        s = Stream(*TEST_VALUES)
        s = s.through(p)
        for t1, t2 in zip(s, TEST_VALUES):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            self.assertEqual(t1, t2)

    def test_fork_multiple(self):
        p = Pipe().fork(TEST_FILTER, TEST_FUNCTION, lambda x: not TEST_FILTER(x), lambda x: TEST_FUNCTION(TEST_FUNCTION(x)))
        s = Stream(*TEST_VALUES)
        s = s.through(p)
        for t1, t2 in zip(s, list(TEST_VALUES)):
            if TEST_FILTER(t2):
                t2 = TEST_FUNCTION(t2)
            else:
                t2 = TEST_FUNCTION(TEST_FUNCTION(t2))
            self.assertEqual(t1, t2)


if __name__ == '__main__':
    unittest.main()
