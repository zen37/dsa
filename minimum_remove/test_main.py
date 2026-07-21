import unittest

from main import minRemoveToMakeValid as min_remove_to_make_valid


def is_valid(s: str) -> bool:
    """Helper: check balanced parentheses (letters ignored)."""
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


class TestMinRemoveToMakeValid(unittest.TestCase):
    """Tests for min_remove_to_make_valid."""

    def test_given_examples(self):
        """The exact examples from the problem statement."""
        self.assertEqual(min_remove_to_make_valid("lee(t(c)o)de)"), "lee(t(c)o)de")
        self.assertEqual(min_remove_to_make_valid("a)b(c)d"), "ab(c)d")
        self.assertEqual(min_remove_to_make_valid("))(("), "")
        self.assertEqual(min_remove_to_make_valid("(a(b(c)d)"), "a(b(c)d)")

    def test_already_valid_unchanged(self):
        """A valid string should come back unchanged."""
        self.assertEqual(min_remove_to_make_valid("(a(b(c)d)e)"), "(a(b(c)d)e)")
        self.assertEqual(min_remove_to_make_valid("abc"), "abc")
        self.assertEqual(min_remove_to_make_valid(""), "")

    def test_only_letters(self):
        """No parentheses at all -- nothing to remove."""
        self.assertEqual(min_remove_to_make_valid("hello"), "hello")

    def test_only_unmatched_closers(self):
        """All ')' with no '(' at all -- every one must go."""
        result = min_remove_to_make_valid(")))")
        self.assertEqual(result, "")
        self.assertTrue(is_valid(result))

    def test_only_unmatched_openers(self):
        """All '(' with no ')' at all -- every one must go."""
        result = min_remove_to_make_valid("(((")
        self.assertEqual(result, "")
        self.assertTrue(is_valid(result))

    def test_mismatched_both_ends(self):
        """The pre-flight edge case: unmatched ')' early AND unmatched '('
        late in the same string. A naive 'trim one end' approach would miss
        one side; this must catch both independently."""
        result = min_remove_to_make_valid("())(")
        self.assertTrue(is_valid(result))
        # minimum removal: drop the extra ')' at index 2 and '(' at index 3
        self.assertEqual(result, "()")

    def test_letters_interspersed_with_bad_brackets(self):
        """Letters must always survive; only brackets are ever removed."""
        result = min_remove_to_make_valid("a)b)c(d")
        self.assertTrue(is_valid(result))
        # letters must all be present, in original relative order
        self.assertEqual([c for c in result if c.isalpha()], ["a", "b", "c", "d"])

    def test_nested_valid_structure_preserved(self):
        """Nested valid parens stay intact when the string is already valid."""
        s = "(a(b)c(d)e)"
        self.assertEqual(min_remove_to_make_valid(s), s)

    def test_single_unmatched_opener(self):
        """One stray '(' at the end -- exactly one char removed."""
        self.assertEqual(min_remove_to_make_valid("abc("), "abc")

    def test_single_unmatched_closer(self):
        """One stray ')' at the start -- exactly one char removed."""
        self.assertEqual(min_remove_to_make_valid(")abc"), "abc")

    def test_result_is_always_valid(self):
        """Property check across several inputs: output must be valid."""
        cases = [
            "lee(t(c)o)de)",
            "a)b(c)d",
            "))((",
            "(a(b(c)d)",
            "()())",
            "(()",
            "))((())",
            "a(b(c)d)e)f(",
        ]
        for s in cases:
            result = min_remove_to_make_valid(s)
            self.assertTrue(is_valid(result), f"invalid result for {s!r}: {result!r}")


if __name__ == "__main__":
    unittest.main()
