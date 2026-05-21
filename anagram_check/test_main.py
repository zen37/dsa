from pathlib import Path
import unittest

from main import get_max_input_length_from_config, is_anagram

TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestIsAnagram(unittest.TestCase):
    def test_returns_true_for_simple_anagrams(self) -> None:
        self.assertTrue(is_anagram("listen", "silent"))

    def test_ignores_case(self) -> None:
        self.assertTrue(is_anagram("Listen", "Silent"))

    def test_ignores_spaces(self) -> None:
        self.assertTrue(is_anagram("dirty room", "Dormitory"))

    def test_returns_false_for_different_characters(self) -> None:
        self.assertFalse(is_anagram("hello", "world"))

    def test_returns_false_when_character_counts_differ(self) -> None:
        self.assertFalse(is_anagram("aabb", "abbb"))

    def test_does_not_ignore_punctuation(self) -> None:
        self.assertFalse(is_anagram("Listen!", "Silent,"))

    def test_supports_unicode_casefolding(self) -> None:
        self.assertTrue(is_anagram("Straße", "STRASSE"))

    def test_supports_arabic_anagrams(self) -> None:
        self.assertTrue(is_anagram("سلام", "مالس"))

    def test_supports_cyrillic_casefolding(self) -> None:
        self.assertTrue(is_anagram("Москва", "Васком"))

    def test_supports_japanese_anagrams(self) -> None:
        self.assertTrue(is_anagram("こんにちは", "はちにんこ"))

    def test_supports_chinese_anagrams_with_spaces(self) -> None:
        self.assertTrue(is_anagram("你好 世界", "界世好你"))

    def test_supports_emoji_anagrams(self) -> None:
        self.assertTrue(is_anagram("😀🔥🚀", "🚀😀🔥"))

    def test_supports_text_and_emoji_anagrams(self) -> None:
        self.assertTrue(is_anagram("Code 🚀", "🚀 doce"))

    def test_allows_inputs_at_configured_max_length(self) -> None:
        max_input_length: int = get_max_input_length_from_config()

        self.assertTrue(is_anagram("a" * max_input_length, "a" * max_input_length))

    def test_raises_error_when_either_input_is_too_long(self) -> None:
        max_input_length: int = get_max_input_length_from_config()
        oversized_input: str = "a" * (max_input_length + 1)

        with self.assertRaises(ValueError):
            is_anagram(oversized_input, "a")

        with self.assertRaises(ValueError):
            is_anagram("a", oversized_input)

    def test_long_file_inputs_are_anagrams(self) -> None:
        s1: str = (TEST_DATA_DIR / "s1.txt").read_text()
        s2: str = (TEST_DATA_DIR / "s2.txt").read_text()

        self.assertTrue(is_anagram(s1, s2))


if __name__ == "__main__":
    unittest.main()
