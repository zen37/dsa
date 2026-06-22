import unittest

from main import find_disappeared_numbers


class TestFindDisappearedNumbers(unittest.TestCase):
    """Tests for find_disappeared_numbers."""

    def test_canonical_example(self):
        """The standard LeetCode example."""
        self.assertEqual(
            find_disappeared_numbers([4, 3, 2, 7, 8, 2, 3, 1]),
            [5, 6],
        )

    def test_small_example(self):
        """A short input with duplicates."""
        self.assertEqual(find_disappeared_numbers([1, 1]), [2])

    def test_none_missing(self):
        """A full permutation of 1..n -> nothing missing."""
        self.assertEqual(find_disappeared_numbers([1, 2, 3, 4]), [])
        self.assertEqual(find_disappeared_numbers([4, 2, 1, 3]), [])

    def test_all_same_value(self):
        """Every element identical -> all other values missing."""
        self.assertEqual(find_disappeared_numbers([2, 2, 2]), [1, 3])
        self.assertEqual(find_disappeared_numbers([1, 1, 1]), [2, 3])

    def test_single_element(self):
        """Length-1 inputs (n == 1, so the only value must be 1)."""
        self.assertEqual(find_disappeared_numbers([1]), [])

    def test_missing_at_ends(self):
        """Missing values at the low and high ends of the range."""
        self.assertEqual(find_disappeared_numbers([2, 2, 3, 4]), [1])  # missing 1
        self.assertEqual(find_disappeared_numbers([1, 2, 3, 3]), [4])  # missing 4

    def test_result_is_sorted(self):
        """Output is ascending regardless of input order."""
        self.assertEqual(
            find_disappeared_numbers([8, 8, 1, 1, 1, 1, 1, 1]),
            [2, 3, 4, 5, 6, 7],
        )

    def test_larger_input(self):
        """A larger range with a known set removed."""
        n = 100
        removed = {17, 42, 99}
        # build a length-n list over [1, n] that omits `removed`,
        # padding with duplicates of a present value to keep length == n.
        present = [v for v in range(1, n + 1) if v not in removed]
        nums = present + [1] * len(removed)  # pad with 1s to restore length n
        self.assertEqual(len(nums), n)
        self.assertEqual(find_disappeared_numbers(nums), sorted(removed))


if __name__ == "__main__":
    unittest.main()
