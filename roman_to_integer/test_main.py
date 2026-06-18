import unittest

from main import roman_to_int


class TestRomanToInt(unittest.TestCase):
    """Tests for roman_to_int."""

    def test_given_examples(self):
        """The examples from the problem statement."""
        self.assertEqual(roman_to_int("III"), 3)
        self.assertEqual(roman_to_int("IV"), 4)
        self.assertEqual(roman_to_int("IX"), 9)
        self.assertEqual(roman_to_int("LVIII"), 58)
        self.assertEqual(roman_to_int("MCMXCIV"), 1994)

    def test_single_symbols(self):
        """Each individual symbol maps to its base value."""
        self.assertEqual(roman_to_int("I"), 1)
        self.assertEqual(roman_to_int("V"), 5)
        self.assertEqual(roman_to_int("X"), 10)
        self.assertEqual(roman_to_int("L"), 50)
        self.assertEqual(roman_to_int("C"), 100)
        self.assertEqual(roman_to_int("D"), 500)
        self.assertEqual(roman_to_int("M"), 1000)

    def test_all_subtractive_forms(self):
        """The six subtractive pairs."""
        self.assertEqual(roman_to_int("IV"), 4)
        self.assertEqual(roman_to_int("IX"), 9)
        self.assertEqual(roman_to_int("XL"), 40)
        self.assertEqual(roman_to_int("XC"), 90)
        self.assertEqual(roman_to_int("CD"), 400)
        self.assertEqual(roman_to_int("CM"), 900)

    def test_pure_additive(self):
        """Numerals with no subtractive pairs."""
        self.assertEqual(roman_to_int("II"), 2)
        self.assertEqual(roman_to_int("VI"), 6)
        self.assertEqual(roman_to_int("XV"), 15)
        self.assertEqual(roman_to_int("LXVI"), 66)
        self.assertEqual(roman_to_int("MMVII"), 2007)

    def test_repeated_symbols(self):
        """Up to three repeats of a symbol."""
        self.assertEqual(roman_to_int("XXX"), 30)
        self.assertEqual(roman_to_int("CCC"), 300)
        self.assertEqual(roman_to_int("MMM"), 3000)

    def test_multiple_subtractive_in_one_numeral(self):
        """Several subtractive pairs within a single numeral."""
        self.assertEqual(roman_to_int("XCIX"), 99)     # 90 + 9
        self.assertEqual(roman_to_int("CDXLIV"), 444)  # 400 + 40 + 4
        self.assertEqual(roman_to_int("CMXLIX"), 949)  # 900 + 40 + 9

    def test_boundaries(self):
        """Smallest and largest representable values."""
        self.assertEqual(roman_to_int("I"), 1)
        self.assertEqual(roman_to_int("MMMCMXCIX"), 3999)  # max in range

    def test_assorted_values(self):
        """A spread of mid-range numerals."""
        self.assertEqual(roman_to_int("XLII"), 42)
        self.assertEqual(roman_to_int("XCIV"), 94)
        self.assertEqual(roman_to_int("DCCCXC"), 890)
        self.assertEqual(roman_to_int("MCDLXXVI"), 1476)
        self.assertEqual(roman_to_int("MMXXIV"), 2024)


if __name__ == "__main__":
    unittest.main()
