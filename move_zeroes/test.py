# test_move_zeros.py
import unittest
from main import move_zeros


class TestMoveZeros(unittest.TestCase):
    # Basic cases
    def test_zeros_in_middle(self):
        self.assertEqual(move_zeros([0, 1, 0, 3, 12]), [1, 3, 12, 0, 0])

    def test_zeros_at_start(self):
        self.assertEqual(move_zeros([0, 0, 1, 2, 3]), [1, 2, 3, 0, 0])

    def test_zeros_at_end(self):
        self.assertEqual(move_zeros([1, 2, 3, 0, 0]), [1, 2, 3, 0, 0])

    def test_single_zero(self):
        self.assertEqual(move_zeros([1, 0, 2]), [1, 2, 0])

    # Edge cases
    def test_no_zeros(self):
        self.assertEqual(move_zeros([1, 2, 3]), [1, 2, 3])

    def test_all_zeros(self):
        self.assertEqual(move_zeros([0, 0, 0]), [0, 0, 0])

    def test_single_zero_only(self):
        self.assertEqual(move_zeros([0]), [0])

    def test_single_non_zero(self):
        self.assertEqual(move_zeros([1]), [1])

    def test_empty_list(self):
        self.assertEqual(move_zeros([]), [])

    def test_order_maintained(self):
        self.assertEqual(move_zeros([3, 0, 1, 0, 2]), [3, 1, 2, 0, 0])


if __name__ == "__main__":
    unittest.main()
