import unittest

from main import calculate


class TestCalculate(unittest.TestCase):
    """Tests for calculate. Grammar: non-negative integers, '+', '-',
    '(', ')', and spaces."""

    # ---- digits / '+' / '-' only (no brackets) ----

    def test_given_example_simple_addition(self):
        """Basic case."""
        self.assertEqual(calculate("1 + 1"), 2)

    def test_given_example_mixed_sign(self):
        """From the problem statement: mid-expression subtraction must be
        applied with its sign, not just the final term."""
        self.assertEqual(calculate(" 2-1 + 2 "), 3)

    def test_subtract_then_add_minimal_case(self):
        """1 - 2 + 3 = 2. The '-2' must stay negative even though a '+'
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
        """Chain of additions."""
        self.assertEqual(calculate("1+2+3+4"), 10)

    def test_subtraction_in_the_middle_only(self):
        """A single subtraction sandwiched between additions:
        5+3-2+1 = 7. The '-2' flush happens on the following '+'."""
        self.assertEqual(calculate("5+3-2+1"), 7)

    # ---- parentheses ----

    def test_given_example_parentheses(self):
        """From the problem statement -- nested groups with sign flips."""
        self.assertEqual(calculate("(1+(4+5+2)-3)+(6+8)"), 23)

    def test_simple_parentheses_no_nesting(self):
        """A single, non-nested group: 1+(2+3) = 6."""
        self.assertEqual(calculate("1+(2+3)"), 6)

    def test_unary_minus_before_parentheses(self):
        """A '-' immediately before a group negates the WHOLE group,
        not just its first term: -(3-4) = 1."""
        self.assertEqual(calculate("-(3-4)"), 1)

    def test_minus_before_group_only_negates_group(self):
        """2-(1+2) = -1. Confirms the '-' applies to the entire group's
        result, not just the group's first term."""
        self.assertEqual(calculate("2-(1+2)"), -1)

    def test_nested_parentheses(self):
        """Multiple levels of nesting, each with its own sign."""
        self.assertEqual(calculate("(1-(2-(3-4)))"), -2)

    def test_parentheses_with_no_sign_before(self):
        """A '(' with an implicit '+' before it (start of string)."""
        self.assertEqual(calculate("(1+2)+3"), 6)

    def test_empty_parentheses_like_group_with_zero(self):
        """A group evaluating to 0 shouldn't disturb the outer sign."""
        self.assertEqual(calculate("5-(2-2)+1"), 6)

    def test_deeply_nested_all_same_sign(self):
        """Deep nesting stresses the stack; all '+' keeps this simple to
        verify by hand: ((((1+2)+3)+4)+5) = 15."""
        self.assertEqual(calculate("((((1+2)+3)+4)+5)"), 15)


if __name__ == "__main__":
    unittest.main()
