def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to its integer value.

    Iterates left to right. Each symbol is added, except when a symbol's value
    is smaller than the symbol immediately after it: in that case the pair is a
    subtractive form (e.g. "IV" = 4, "CM" = 900), so the smaller value is
    subtracted instead of added.

    Constraints:
        - s contains only the symbols I, V, X, L, C, D, M.
        - s is a valid Roman numeral representing a number in [1, 3999].
        - 1 <= len(s) <= 15.

    Args:
        s: A valid Roman numeral string.

    Returns:
        The integer value of the numeral.

    Complexity:
        n = len(s).
        Time:  O(n) - single pass over the string.
        Space: O(1) - fixed-size value table; no scaling allocation.
    """
    values: dict[str, int] = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    total: int = 0
    for i in range(len(s)):
        current: int = values[s[i]]
        # If a smaller value precedes a larger one, it is subtractive.
        if i + 1 < len(s) and current < values[s[i + 1]]:
            total -= current
        else:
            total += current

    return total


if __name__ == "__main__":
    # Example usage:
    print(roman_to_int("III"))  # Output: 3
    print(roman_to_int("IV"))  # Output: 4
    print(roman_to_int("IX"))  # Output: 9
    print(roman_to_int("LVIII"))  # Output: 58
    print(roman_to_int("MCMXCIV"))  # Output: 1994
