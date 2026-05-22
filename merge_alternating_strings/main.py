def merge_alternate(word1: str, word2: str) -> str:
    """
    Return a string built by alternating characters from word1 and word2.

    Characters are taken in lockstep from both words; once the shorter
    word is exhausted, the remaining characters of the longer word are appended.

    Time: O(n + m), where n and m are the lengths of word1 and word2.
    Space: O(n + m) for the merged result.
    """
    merged: list[str] = []

    shorter_length: int = min(len(word1), len(word2))

    for i in range(shorter_length):
        merged.append(word1[i])
        merged.append(word2[i])

    # Append the leftover tail from whichever word is longer
    # (one of these slices will be empty, so this is safe).
    merged.append(word1[shorter_length:])
    merged.append(word2[shorter_length:])

    return "".join(merged)


if __name__ == "__main__":
    print(merge_alternate("abc", "pqr"))
    print(merge_alternate("ab", "pqrs"))
    print(merge_alternate("abcd", "pq"))
    print(merge_alternate("x", "pq 3 n3333 3"))
    print(merge_alternate("    ", ""))
