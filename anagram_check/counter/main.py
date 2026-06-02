from collections import Counter


def is_anagram(s1: str, s2: str) -> bool:
    """
    Return True if two strings are anagrams, ignoring case and spaces.

    Time: O(n + m), where n and m are the cleaned string lengths.
    Space: O(k), where k is the number of unique cleaned characters.
    """
    cleaned_s1: str = s1.lower().replace(" ", "")
    cleaned_s2: str = s2.lower().replace(" ", "")

    return Counter(cleaned_s1) == Counter(cleaned_s2)


if __name__ == "__main__":
    print(is_anagram("ssdsdds", "ddd"))
    print(is_anagram("silent", "listen"))
