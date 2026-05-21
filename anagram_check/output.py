from config import get_max_display_length_from_config
from core import is_anagram


def format_for_display(
    text: str, *, show_full_text: bool = False, more_text: int = 0
) -> str:
    """
    Return text shortened to the configured display length.

    Time: O(d), Space: O(d), where d is the configured display length plus
    any extra requested text.
    """
    if show_full_text:
        return text

    if more_text < 0:
        raise ValueError("more_text must be at least 0.")

    max_display_length: int = get_max_display_length_from_config() + more_text

    if len(text) <= max_display_length:
        return text

    hidden_char_count: int = len(text) - max_display_length

    return f"{text[:max_display_length]}... [{hidden_char_count} more chars]"


def print_anagram_result(
    s1: str, s2: str, *, show_full_text: bool = False, more_text: int = 0
) -> None:
    """
    Print whether two strings are anagrams after cleaning.
    """
    displayed_s1: str = format_for_display(
        s1,
        show_full_text=show_full_text,
        more_text=more_text,
    )
    displayed_s2: str = format_for_display(
        s2,
        show_full_text=show_full_text,
        more_text=more_text,
    )

    if is_anagram(s1, s2):
        print(f'✅ "{displayed_s1}" and "{displayed_s2}" are anagrams.')
    else:
        print(f'❌ "{displayed_s1}" and "{displayed_s2}" are not anagrams.')
