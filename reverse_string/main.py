def reverse_string_v1(s: str) -> str:
    """reverses the string received as argument"""
    # Time: O(n), Space: O(n) — explicit loop in Python; builds result list then joins

    result: list[str] = []
    for i in range(len(s) - 1, -1, -1):
        result.append(s[i])

    return "".join(result)


def reverse_string_v2(s: str) -> str:
    """reverses the string received as argument"""
    # Time: O(n), Space: O(n) — fastest in practice; slice reversal runs in C (CPython)
    return s[::-1]


def reverse_string(s: str) -> str:
    """reverses the string received as argument"""
    # Time: O(n), Space: O(n) — reversed() is a lazy iterator; no intermediate list allocated
    return "".join(reversed(s))


if __name__ == "__main__":
    print(reverse_string("hello world"))
