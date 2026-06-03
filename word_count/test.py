import pytest

from main import word_count

# --- Test Cases ---


class TestWordCount:
    # Basic functionality
    def test_example(self):
        assert word_count(["apple", "banana", "apple", "cherry"]) == {
            "apple": 2,
            "banana": 1,
            "cherry": 1,
        }

    def test_all_unique(self):
        assert word_count(["apple", "banana", "cherry"]) == {
            "apple": 1,
            "banana": 1,
            "cherry": 1,
        }

    def test_all_same(self):
        assert word_count(["apple", "apple", "apple"]) == {"apple": 3}

    def test_single_element(self):
        assert word_count(["apple"]) == {"apple": 1}

    # Edge cases
    def test_empty_list(self):
        assert word_count([]) == {}

    def test_two_words(self):
        assert word_count(["a", "b"]) == {"a": 1, "b": 1}

    def test_large_count(self):
        assert word_count(["x"] * 1000) == {"x": 1000}

    # Case sensitivity
    def test_case_sensitive(self):
        assert word_count(["Apple", "apple", "APPLE"]) == {
            "Apple": 1,
            "apple": 1,
            "APPLE": 1,
        }

    # Whitespace and special strings
    def test_strings_with_spaces(self):
        assert word_count(["hello world", "hello world", "hi"]) == {
            "hello world": 2,
            "hi": 1,
        }

    def test_empty_string_as_word(self):
        assert word_count(["", "", "apple"]) == {"": 2, "apple": 1}

    def test_numeric_strings(self):
        assert word_count(["1", "2", "1"]) == {"1": 2, "2": 1}

    def test_special_characters(self):
        assert word_count(["!", "!", "?"]) == {"!": 2, "?": 1}

    # Order independence — counts correct regardless of input order
    def test_order_independence(self):
        assert word_count(["banana", "apple", "banana"]) == {"banana": 2, "apple": 1}

    def test_interleaved_words(self):
        assert word_count(["a", "b", "a", "b", "a"]) == {"a": 3, "b": 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
