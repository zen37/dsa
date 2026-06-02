def is_anagram(s1: str, s2: str) -> bool:
    """
    Return True if two strings are anagrams, ignoring case and spaces.

    Time: O(n log n + m log m), where n and m are the cleaned string lengths.
    Space: O(n + m).
    """
    cleaned_s1: str = s1.lower().replace(" ", "")
    cleaned_s2: str = s2.lower().replace(" ", "")

    return sorted(cleaned_s1) == sorted(cleaned_s2)


if __name__ == "__main__":
    print(is_anagram("ssdsdds", "ddd"))
    print(is_anagram("silent", "listen"))
