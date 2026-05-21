def get_ignored_chars_from_config() -> set[str]:
    """
    Return characters ignored during anagram comparison.

    Pretend this value is read from config.
    """
    return {" "}


def get_case_normalizer_name_from_config() -> str:
    """
    Return the configured case normalization mode.

    Pretend this value is read from config.

    Supported values:
    - "exact": preserve original text
    - "lower": use basic lowercase comparison
    - "casefold": use Unicode-friendly case-insensitive comparison
    """
    return "casefold"


def get_max_input_length_from_config() -> int:
    """
    Return the maximum allowed input string length.

    Pretend this value is read from config.
    """
    return 1000


def get_max_display_length_from_config() -> int:
    """
    Return the maximum string length to show in printed output.

    Pretend this value is read from config.
    """
    return 10
