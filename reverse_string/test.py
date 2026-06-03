import pytest

from main import reverse_string


# --- Test Cases ---


class TestReverseString:
    # Basic functionality
    def test_basic_word(self):
        assert reverse_string("hello") == "olleh"

    def test_single_character(self):
        assert reverse_string("a") == "a"

    def test_two_characters(self):
        assert reverse_string("ab") == "ba"

    # Edge cases
    def test_empty_string(self):
        assert reverse_string("") == ""

    def test_palindrome(self):
        assert reverse_string("racecar") == "racecar"

    def test_spaces(self):
        assert reverse_string("hello world") == "dlrow olleh"

    def test_leading_trailing_spaces(self):
        assert reverse_string("  hi  ") == "  ih  "

    # Special characters
    def test_punctuation(self):
        assert reverse_string("hello!") == "!olleh"

    def test_numbers_in_string(self):
        assert reverse_string("abc123") == "321cba"

    def test_numeric_string(self):
        assert reverse_string("12345") == "54321"

    def test_special_characters(self):
        assert reverse_string("!@#$%") == "%$#@!"

    # Case sensitivity
    def test_uppercase(self):
        assert reverse_string("HELLO") == "OLLEH"

    def test_mixed_case(self):
        assert reverse_string("HeLLo") == "oLLeH"

    # Unicode / whitespace
    def test_newline_character(self):
        assert reverse_string("hi\nbye") == "eyb\nih"

    def test_unicode_characters(self):
        assert reverse_string("héllo") == "olléh"

    def test_emoji(self):
        assert reverse_string("hi😊") == "😊ih"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
