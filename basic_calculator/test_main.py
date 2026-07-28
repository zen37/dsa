import unittest

from main import calculate


class TestCalculate(unittest.TestCase):
    """Tests for calculate, scoped to the actual input grammar: digits,
    '+', '-', and spaces only -- no parentheses.

    NOTE: this implementation has a real bug (see below) and several tests
    will FAIL as submitted.
    """

    def test_given_example_simple_addition(self):
        """Basic case: passes today."""
        self.assertEqual(calculate("1 + 1"), 2)

    def test_given_example_mixed_sign(self):
        """From the problem statement. Exposes the bug: mid-expression
        subtraction is not applied with its sign when a later operator
        triggers the flush -- only the LAST term gets sign-multiplied."""
        self.assertEqual(calculate(" 2-1 + 2 "), 3)

    def test_subtract_then_add_minimal_case(self):
        """Minimal, isolated reproduction of the bug.
        1 - 2 + 3 = 2. The '-2' must stay negative even though a '+'
        comes after it and triggers its flush."""
        self.assertEqual(calculate("1-2+3"), 2)

    def test_multiple_subtractions_in_a_row(self):
        """Chained subtraction: 10 - 2 - 3 = 5."""
        self.assertEqual(calculate("10-2-3"), 5)

    def test_leading_unary_minus(self):
        """A leading '-' with no operand before it: -5+3 = -2."""
        self.assertEqual(calculate("-5+3"), -2)

    def test_single_number_no_operators(self):
        """No operators at all -- exercises only the final flush."""
        self.assertEqual(calculate("42"), 42)

    def test_all_additions(self):
        """Chain of additions -- passes today (no sign issue exposed)."""
        self.assertEqual(calculate("1+2+3+4"), 10)

    def test_subtraction_in_the_middle_only(self):
        """A single subtraction sandwiched between additions:
        5+3-2+1 = 7. The '-2' flush happens on the following '+',
        which is exactly the bug's trigger condition."""
        self.assertEqual(calculate("5+3-2+1"), 7)


if __name__ == "__main__":
    unittest.main()
