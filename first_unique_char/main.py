def first_unique_char(s: str) -> int:
    # Time O(n) + n*O(1) + n*O(1) + O(n) = O(n)
    # Space O(n) + O(n) = O(n)

    s_dict: dict[str, int] = {}
    s_pos_dict: dict[str, int] = {}

    for i, char in enumerate(s):
        s_dict[char] = s_dict.get(char, 0) + 1
        if s_pos_dict.get(char, 0) == 0:
            s_pos_dict[char] = i

    for char in s_dict:
        if s_dict[char] == 1:
            return s_pos_dict[char]

    return -1


def first_unique_char_claude(s: str) -> int:
    # Time: O(n); Space: O(n)
    counts: dict[str, int] = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for i, char in enumerate(s):
        if counts[char] == 1:
            return i

    return -1


if __name__ == "__main__":
    print(first_unique_char("leetcode"))
    print(first_unique_char("loveleetcode"))
    print(first_unique_char("aabb"))
    print(first_unique_char("z"))
    print(first_unique_char("abad"))
