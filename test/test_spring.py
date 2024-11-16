import unittest

from stream import Spring

TEST_VALUES = range(100)


class TestSpring(unittest.TestCase):
    def test_init(self):
        s = Spring()
        self.assertTrue(isinstance(s, Spring))

    def test_run_blank(self):
        s = Spring()
        for t in s.take(5):
            self.assertEqual(t, None)

    def test_run_with_values(self):
        s = Spring(TEST_VALUES)
        for t in TEST_VALUES:
            self.assertEqual(next(s), t)

    def test_run_with_values_repeat(self):
        s = Spring(TEST_VALUES)
        for t in TEST_VALUES:
            self.assertEqual(next(s), t)
        for t in TEST_VALUES:
            self.assertEqual(next(s), t)


if __name__ == "__main__":
    unittest.main()
