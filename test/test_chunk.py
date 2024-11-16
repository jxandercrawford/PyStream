import unittest

from stream import Chunk

TEST_VALUES = range(100)
TEST_FUNCTION = lambda x: x * -1
TEST_INDEX = 10


class TestChunk(unittest.TestCase):
    def test_init(self):
        c = Chunk()
        self.assertTrue(isinstance(c, Chunk))

    def test_length_empty(self):
        c = Chunk()
        self.assertEqual(len(c), 0)

    def test_run_with_values(self):
        c = Chunk(*TEST_VALUES)
        for t1, t2 in zip(c, TEST_VALUES):
            self.assertEqual(t1, t2)

    def test_indexing(self):
        c = Chunk(*TEST_VALUES)
        self.assertEqual(c[TEST_INDEX], list(TEST_VALUES)[TEST_INDEX])

    def test_map(self):
        c = Chunk(*TEST_VALUES)
        c = c.map(TEST_FUNCTION)
        for t1, t2 in zip(c, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(t2))

    def test_map_twice(self):
        c = Chunk(*TEST_VALUES)
        c = c.map(TEST_FUNCTION).map(TEST_FUNCTION)
        for t1, t2 in zip(c, TEST_VALUES):
            self.assertEqual(t1, TEST_FUNCTION(TEST_FUNCTION(t2)))


if __name__ == "__main__":
    unittest.main()
