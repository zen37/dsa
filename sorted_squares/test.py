import unittest

from main import sorted_squares


class TestSortedSquares(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(sorted_squares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])

    def test_example_2(self):
        self.assertEqual(
            sorted_squares([-7, -3, 2, 3, 11, 15]), [4, 9, 9, 49, 121, 225]
        )

    def test_all_negative(self):
        self.assertEqual(sorted_squares([-5, -3, -2, -1]), [1, 4, 9, 25])

    def test_mixed_with_zero(self):
        self.assertEqual(sorted_squares([-1, 0, 1]), [0, 1, 1])

    def test_duplicates(self):
        self.assertEqual(sorted_squares([-1, -1, 0, 1, 1]), [0, 1, 1, 1, 1])

    def test_single_negative(self):
        self.assertEqual(sorted_squares([-2]), [4])

    def test_single_zero(self):
        self.assertEqual(sorted_squares([0]), [0])

    def test_all_equal_in_abs(self):
        self.assertEqual(sorted_squares([-2, -2, 2, 2]), [4, 4, 4, 4])

    def test_single_positive(self):
        self.assertEqual(sorted_squares([5]), [25])

    def test_all_positive(self):
        self.assertEqual(sorted_squares([1, 2, 3, 4]), [1, 4, 9, 16])

    def test_all_zeros(self):
        self.assertEqual(sorted_squares([0, 0, 0]), [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
