import unittest

from main import missing_number


class TestMissingNumber(unittest.TestCase):
    """Tests for missing_number."""

    def test_given_examples(self):
        """The examples from the problem statement."""
        self.assertEqual(missing_number([3, 0, 1]), 2)
        self.assertEqual(missing_number([0, 1]), 2)
        self.assertEqual(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)
        self.assertEqual(missing_number([0]), 1)
        self.assertEqual(missing_number([1]), 0)

    def test_missing_is_zero(self):
        """The absent value is 0 (the low end of the range)."""
        self.assertEqual(missing_number([1]), 0)
        self.assertEqual(missing_number([1, 2]), 0)
        self.assertEqual(missing_number([2, 1, 3]), 0)

    def test_missing_is_n(self):
        """The absent value is n (the high end of the range)."""
        self.assertEqual(missing_number([0]), 1)
        self.assertEqual(missing_number([0, 1]), 2)
        self.assertEqual(missing_number([0, 1, 2]), 3)

    def test_missing_in_middle(self):
        """The absent value lies strictly inside the range."""
        self.assertEqual(missing_number([0, 1, 3]), 2)
        self.assertEqual(missing_number([0, 2, 3, 4]), 1)
        self.assertEqual(missing_number([0, 1, 2, 4, 5]), 3)

    def test_order_independence(self):
        """The result is independent of input ordering."""
        self.assertEqual(missing_number([0, 1, 3, 4]), 2)
        self.assertEqual(missing_number([4, 3, 1, 0]), 2)
        self.assertEqual(missing_number([3, 0, 4, 1]), 2)

    def test_larger_input(self):
        """A larger, fully shuffled range with one value removed."""
        full = list(range(101))      # 0..100, so n = 100
        removed = 57
        nums = [x for x in full if x != removed]
        # nums now has length 100 (== n), range [0, 100], missing 57
        import random
        random.shuffle(nums)
        self.assertEqual(missing_number(nums), removed)

    def test_single_element_both_cases(self):
        """Length-1 inputs: only [0] (missing 1) or [1] (missing 0)."""
        self.assertEqual(missing_number([0]), 1)
        self.assertEqual(missing_number([1]), 0)


if __name__ == "__main__":
    unittest.main()
