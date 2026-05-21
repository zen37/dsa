from config import (
    get_case_normalizer_name_from_config,
    get_ignored_chars_from_config,
    get_max_input_length_from_config,
)


def validate_input_lengths(s1: str, s2: str) -> None:
    """
    Raise ValueError if either input string is longer than the configured limit.

    Time: O(1), Space: O(1).
    """
    max_input_length: int = get_max_input_length_from_config()

    if len(s1) > max_input_length or len(s2) > max_input_length:
        raise ValueError(
            f"Input strings must be at most {max_input_length} characters long."
        )


def normalize_case(text: str) -> str:
    """
    Apply the configured case normalization rule.

    Time: O(n), Space: O(n), where n is the length of text.
    """
    normalizer_name: str = get_case_normalizer_name_from_config()

    if normalizer_name == "exact":
        return text

    if normalizer_name == "lower":
        return text.lower()

    if normalizer_name == "casefold":
        return text.casefold()

    raise ValueError(f"Unknown case normalizer: {normalizer_name}")


def clean_text(text: str) -> str:
    """
    Remove ignored characters and apply configured case normalization.

    Time: O(n), Space: O(n), where n is the length of text.
    """
    ignored_chars: set[str] = get_ignored_chars_from_config()

    text_without_ignored_chars: str = "".join(
        char for char in text if char not in ignored_chars
    )

    return normalize_case(text_without_ignored_chars)


def is_anagram(s1: str, s2: str) -> bool:
    """
    Return True if two strings are anagrams after cleaning.

    The comparison ignores configured characters and applies the configured
    case normalization rule.

    Time: O(n + m), where n and m are the lengths of the input strings.
    Space: O(n + m + k), where k is the number of unique cleaned characters.
    """
    validate_input_lengths(s1, s2)

    cleaned_s1: str = clean_text(s1)
    cleaned_s2: str = clean_text(s2)

    # Anagrams must have the same length; bail early to skip the counting work.
    if len(cleaned_s1) != len(cleaned_s2):
        return False

    # Build a frequency table of characters in s1. Each char in s2 decrements
    # its count; if no matching character remains, the multisets differ.
    remaining_counts: dict[str, int] = {}

    for char in cleaned_s1:
        remaining_counts[char] = remaining_counts.get(char, 0) + 1

    for char in cleaned_s2:
        # Covers both cases in one check: char is absent from s1's frequency
        # table, or its count has already been decremented to zero.
        if remaining_counts.get(char, 0) == 0:
            return False

        remaining_counts[char] -= 1

    # Lengths matched and every decrement succeeded, so all counts are now
    # exactly zero — the two character multisets are equal.
    return True
