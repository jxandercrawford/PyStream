import unittest
from main.src.stream import Pipe

TEST_VALUE = 2
TEST_FUNCTION_1 = lambda x: x * 2


class TestPipe(unittest.TestCase):
    def test_init(self):
        p = Pipe()
        self.assertTrue(isinstance(p, Pipe))

    def test_init_blank(self):
        p = Pipe()
        self.assertEqual(p(TEST_VALUE), TEST_VALUE)

    def test_init_1_function(self):
        p = Pipe(TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_VALUE))

    def test_init_2_functions(self):
        p = Pipe(TEST_FUNCTION_1, TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_VALUE)))

    def test_init_3_functions(self):
        p = Pipe(TEST_FUNCTION_1, TEST_FUNCTION_1, TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_VALUE))))

    def test_through_1_time(self):
        p = Pipe()
        p = p.through(TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_VALUE))

    def test_through_2_times(self):
        p = Pipe()
        p = p.through(TEST_FUNCTION_1)
        p = p.through(TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_VALUE)))

    def test_through_3_times(self):
        p = Pipe()
        p = p.through(TEST_FUNCTION_1)
        p = p.through(TEST_FUNCTION_1)
        p = p.through(TEST_FUNCTION_1)
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_FUNCTION_1(TEST_VALUE))))

    def test_addition_of_pipe(self):
        p1 = Pipe()
        p2 = Pipe(TEST_FUNCTION_1)
        p1 += p2
        val = p1(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_VALUE))

    def test_addition_of_function(self):
        p = Pipe()
        p += TEST_FUNCTION_1
        val = p(TEST_VALUE)
        self.assertEqual(val, TEST_FUNCTION_1(TEST_VALUE))


if __name__ == '__main__':
    unittest.main()
