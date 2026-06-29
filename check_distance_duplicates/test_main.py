import unittest

from main import check_distance_duplicates


class TestContainsNearbyDuplicate(unittest.TestCase):
    """Tests for contains_nearby_duplicate."""

    def test_canonical_examples(self):
        """The standard LeetCode examples."""
        self.assertTrue(check_distance_duplicates([1, 2, 3, 1], 3))
        self.assertTrue(check_distance_duplicates([1, 0, 1, 1], 1))
        self.assertFalse(check_distance_duplicates([1, 2, 3, 1, 2, 3], 2))

    def test_no_duplicates_at_all(self):
        """All-distinct values can never satisfy the condition."""
        self.assertFalse(check_distance_duplicates([1, 2, 3, 4, 5], 3))
        self.assertFalse(check_distance_duplicates([1, 2, 3, 4, 5], 100))

    def test_duplicate_exactly_at_distance_k(self):
        """abs(i - j) == k is allowed (boundary is inclusive)."""
        # equal values at indices 0 and 3 -> distance 3
        self.assertTrue(check_distance_duplicates([1, 2, 3, 1], 3))

    def test_duplicate_just_beyond_k(self):
        """abs(i - j) == k + 1 must fail."""
        # equal values at indices 0 and 3 -> distance 3, but k = 2
        self.assertFalse(check_distance_duplicates([1, 2, 3, 1], 2))

    def test_adjacent_duplicates(self):
        """Equal values side by side -> distance 1."""
        self.assertTrue(check_distance_duplicates([1, 1], 1))
        self.assertTrue(check_distance_duplicates([5, 5], 1))
        self.assertFalse(check_distance_duplicates([1, 1], 0))  # k = 0 disallows

    def test_k_zero(self):
        """k == 0 requires distance <= 0, impossible for distinct indices."""
        self.assertFalse(check_distance_duplicates([1, 1, 1], 0))
        self.assertFalse(check_distance_duplicates([1, 2, 3], 0))

    def test_single_element(self):
        """One element has no second index to pair with."""
        self.assertFalse(check_distance_duplicates([7], 1))
        self.assertFalse(check_distance_duplicates([7], 0))

    def test_empty_array(self):
        """No elements -> no pair."""
        self.assertFalse(check_distance_duplicates([], 3))

    def test_duplicate_far_then_near(self):
        """A far-apart pair fails, but a closer pair later succeeds."""
        # 1s at indices 0 and 4 (distance 4) and 4 and 5 (distance 1)
        self.assertTrue(check_distance_duplicates([1, 2, 3, 4, 1, 1], 1))

    def test_negatives_and_zero(self):
        """Values may be negative or zero."""
        self.assertTrue(check_distance_duplicates([-1, 0, -1], 2))
        self.assertFalse(check_distance_duplicates([-1, 0, -1], 1))
        self.assertTrue(check_distance_duplicates([0, 0], 1))

    def test_large_k_covers_whole_array(self):
        """k >= n - 1 means any duplicate anywhere counts."""
        self.assertTrue(check_distance_duplicates([1, 2, 3, 4, 1], 4))
        self.assertTrue(check_distance_duplicates([1, 2, 3, 4, 1], 10))

    def test_multiple_values_repeating(self):
        """Several distinct values repeat; only proximity decides."""
        # 2s at 1 and 3 (distance 2), 3s at 2 and 5 (distance 3)
        self.assertTrue(check_distance_duplicates([1, 2, 3, 2, 4, 3], 2))
        self.assertFalse(check_distance_duplicates([1, 2, 3, 9, 4, 3], 2))  # 3s dist 3


if __name__ == "__main__":
    unittest.main()
