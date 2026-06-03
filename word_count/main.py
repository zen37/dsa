from collections import Counter


def word_count_v2(lst: list[str]) -> dict[str, int]:
    """Returns a dict mapping each word to the number of times it appears in the list."""
    # Time: O(n), Space: O(k) where k = number of unique words
    return dict(Counter(lst))


def word_count_v1(lst: list[str]) -> dict[str, int]:
    """
    Returns a dict mapping each word to the number of times it appears in the list
    """
    # Time: O(n), Space: O(k) where k = number of unique words
    word_dict: dict[str, int] = {}
    for w in lst:
        word_dict[w] = word_dict.get(w, 0) + 1

    return word_dict
