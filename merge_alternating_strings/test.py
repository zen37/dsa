# test_merge_alternate.py
import unittest
from main import merge_alternate


class TestMergeAlternate(unittest.TestCase):
    # Basic cases
    def test_same_length(self):
        self.assertEqual(merge_alternate("abc", "pqr"), "apbqcr")

    def test_word1_shorter(self):
        self.assertEqual(merge_alternate("ab", "pqrs"), "apbqrs")

    def test_word2_shorter(self):
        self.assertEqual(merge_alternate("abcd", "pq"), "apbqcd")

    # Edge cases
    def test_word1_empty(self):
        self.assertEqual(merge_alternate("", "pqr"), "pqr")

    def test_word2_empty(self):
        self.assertEqual(merge_alternate("abc", ""), "abc")

    def test_both_empty(self):
        self.assertEqual(merge_alternate("", ""), "")

    def test_single_char_each(self):
        self.assertEqual(merge_alternate("a", "p"), "ap")

    def test_word1_single_char(self):
        self.assertEqual(merge_alternate("a", "pqr"), "apqr")

    def test_word2_single_char(self):
        self.assertEqual(merge_alternate("abc", "p"), "apbc")


if __name__ == "__main__":
    unittest.main()
