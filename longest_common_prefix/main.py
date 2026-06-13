def longest_common_prefix_1(strs: list[str]) -> str:

    if len(strs) == 0:
        return ""
    if len(strs) == 1:
        return strs[0]

    prefix: str = ""
    chars_dict: dict[str, int] = {}

    for word in strs:
        for i, char in enumerate(word):
            chars_dict[char + str(i)] = chars_dict.get(char + str(i), 0) + 1

    first_char_count = next(iter(chars_dict.values()))
    if first_char_count != len(strs):
        return ""

    for key, value in chars_dict.items():
        if value == len(strs):
            prefix += key
        else:
            break

    return "".join([character for character in prefix if not character.isdigit()])


def longest_common_prefix_2(strs: list[str]) -> str:
    """Return the longest common prefix shared by all strings in ``strs``.

    Vertical scan: walks character positions of the shortest string and, at
    each position, checks whether every string agrees on that character. The
    first disagreement marks the end of the common prefix. Bounding the scan
    by the shortest string guarantees in-range indexing for all words.

    Args:
        strs: List of strings to compare. May be empty.

    Returns:
        The longest common prefix. Empty string if ``strs`` is empty or the
        strings share no common starting character.

    Complexity:
        n = number of strings, m = length of the shortest string.
        Time:  O(n * m) -- worst case compares every word at every position
                           up to the shortest length; exits early on mismatch.
        Space: O(1) extra -- only scalar indices held; output not counted.
    """
    if not strs:
        return ""
    shortest = min(strs, key=len)
    for i, char in enumerate(shortest):
        if any(word[i] != char for word in strs):
            return shortest[:i]
    return shortest


def longest_common_prefix_3(strs: list[str]) -> str:
    """Return the longest common prefix shared by all strings in ``strs``.

    Transposes the strings with ``zip(*strs)``, yielding one column (one
    character from each string) at a time. ``zip`` stops at the shortest
    string automatically, so indexing never overruns. A column extends the
    prefix only if all its characters are identical (``len(set) == 1``); the
    first mixed column ends the prefix.

    Handles edge cases for free: ``zip`` of an empty list yields nothing, and
    ``zip`` of a single string yields one-element columns that always match.

    Args:
        strs: List of strings to compare. May be empty.

    Returns:
        The longest common prefix. Empty string if ``strs`` is empty or the
        strings share no common starting character.

    Complexity:
        n = number of strings, m = length of the shortest string.
        Time:  O(n * m) -- each of up to m columns builds a set of n chars.
        Space: O(n) extra -- one column tuple plus its set, both size n;
                             O(n + m) if the prefix accumulator is counted.
    """
    prefix = []
    for column in zip(*strs):
        if len(set(column)) == 1:
            prefix.append(column[0])
        else:
            break
    return "".join(prefix)


if __name__ == "__main__":
    print(longest_common_prefix(["interview", "interval", "internal"]))  # "inter"
    print(longest_common_prefix(["flower", "flow", "flight"]))  # "fl"
    print(longest_common_prefix(["dog", "racecar", "car"]))  # ""
    print(longest_common_prefix(["aaaaaa", "ab"]))  # "a
    print(longest_common_prefix(["a"]))  # "a"
    print(longest_common_prefix(["ab", "abx", "abcdef"]))  # "a"
