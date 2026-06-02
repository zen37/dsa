def is_anagram(s1: str, s2: str) -> bool:
    """
    Return True if two strings are anagrams, ignoring case and spaces.

    Time: O(n + m), where n and m are the cleaned string lengths.
    Space: O(k), where k is the number of unique cleaned characters.
    """
    cleaned_s1: str = s1.lower().replace(" ", "")
    cleaned_s2: str = s2.lower().replace(" ", "")

    if len(cleaned_s1) != len(cleaned_s2):
        return False

    # Tally of s1's characters, drawn down as s2 is matched against it.
    remaining_counts: dict[str, int] = {}

    # First pass: count how many times each character appears in s1.
    # .get(char, 0) returns the current count or 0 for a new char, then we add 1 for this occurrence.
    for char in cleaned_s1:
        remaining_counts[char] = remaining_counts.get(char, 0) + 1

    # Second pass: each char in s2 consumes one occurrence from s1's tally.
    for char in cleaned_s2:
        # Two failure cases collapsed into one check: the char was never in s1
        # (.get returns 0), or s1 had it but every occurrence has already been
        # consumed (count decremented to 0). Either way, not an anagram.
        if remaining_counts.get(char, 0) == 0:
            return False

        remaining_counts[char] -= 1

    return True


if __name__ == "__main__":
    print(is_anagram("ssdsdds", "ddd"))
    print(is_anagram("silent", "listen"))
