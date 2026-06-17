def longest_common_prefix_1(strs: list[str]) -> str:
    """Return the longest common prefix shared by all strings in ``strs``.

    Counts every (character, position) pair across all strings. A position
    belongs to the common prefix only if its character occurs in every
    string, i.e. its count equals ``len(strs)``. Counting walks the pairs in
    the order the first word introduces them, so appending matching keys
    until the first miss reconstructs the prefix of ``strs[0]``.

    Assumes inputs consist of lowercase English letters only (per the
    ask constraint), so stripping digits from the result removes only
    the encoded position indices.

    Args:
        strs: List of strings to compare. May be empty.

    Returns:
        The longest common prefix. Empty string if ``strs`` is empty or the
        strings share no common starting character.

    Complexity:
        n = number of strings, m = length of the longest string.
        Time:  O(n * m) -- every character of every string is counted once.
        Space: O(n * m) -- the dict holds up to one entry per distinct
                            (character, position) pair.
    """

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


def longest_common_prefix(strs: list[str]) -> str:
    """Return the longest prefix common to every string in strs.

    Uses vertical (column-by-column) scanning: compare the character
    at each position across all strings, stopping at the first mismatch.

    Time:  O(S) where S is the sum of all characters (worst case scans
           every character once).
    Space: O(1) extra (ignoring the output string).
    """
    if not strs:
        return ""

    first = strs[0]
    for i, char in enumerate(first):  # walk columns of the first string
        for other in strs[1:]:  # check the same column in the rest
            if i >= len(other) or other[i] != char:
                return first[:i]  # mismatch or ran off the end
    return first  # first string is a prefix of all


if __name__ == "__main__":
    print(longest_common_prefix(["interview", "interval", "internal"]))  # "inter"
    print(longest_common_prefix(["flower", "flow", "flight"]))  # "fl"
    print(longest_common_prefix(["dog", "racecar", "car"]))  # ""
    print(longest_common_prefix(["aaaaaa", "ab"]))  # "a
    print(longest_common_prefix(["aa", "ba"]))  # ""
    print(longest_common_prefix(["a"]))  # "a"
    print(longest_common_prefix(["ab", "abx", "abcdef"]))  # "ab"
