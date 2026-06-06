import unittest
from main import two_sum


class TestTwoSum(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(set(two_sum([2, 7, 11, 15], 9)), {0, 1})

    def test_another_basic(self):
        self.assertEqual(set(two_sum([3, 2, 4], 6)), {1, 2})

    def test_duplicates(self):
        self.assertEqual(set(two_sum([3, 3], 6)), {0, 1})

    def test_multiple_pairs(self):
        self.assertEqual(set(two_sum([1, 5, 3, 7], 8)), {0, 3})

    def test_negative_numbers(self):
        self.assertEqual(set(two_sum([-1, -2, -3, -4], -6)), {1, 3})

    def test_mixed(self):
        self.assertEqual(set(two_sum([-3, 4, 3, 90], 0)), {0, 2})

    def test_min_case(self):
        self.assertEqual(set(two_sum([1, 2], 3)), {0, 1})


if __name__ == "__main__":
    unittest.main()
