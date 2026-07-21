def minRemoveToMakeValid(s: str) -> str:
    """Remove the minimum number of parentheses so the result is valid.

    Same LIFO invariant as Valid Parentheses -- the stack holds indices of
    unmatched '(' seen so far, innermost on top. What changes from a plain
    validity check: we push INDICES, not characters, and mark exact positions
    for removal instead of returning a bool.

    Pass 1 (scan): for '(' push its index. For ')': if the stack is
    non-empty, pop (it found its match, keep both). If the stack is empty,
    this ')' has no opener -- mark its index for removal immediately.
    After the scan, every index STILL on the stack is an unmatched '(' --
    mark all of those for removal too.

    Pass 2 (rebuild): walk the string again, keeping every character whose
    index was not marked for removal.

    Args:
        s: A string of '(', ')', and lowercase letters.

    Returns:
        A valid string with the minimum number of parentheses removed.

    Complexity:
        n = len(s).
        Time:  O(n) - one scan pass + one rebuild pass.
        Space: O(n) - stack holds up to n indices; remove-set up to n indices.
    """
    stack: list[int] = []
    to_remove: set[int] = set()

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()  # matched -- keep both
            else:
                to_remove.add(i)  # unmatched ')' -- no opener to pair with

    # Whatever '(' indices remain on the stack were never closed.
    to_remove.update(stack)

    result_chars: list[str] = [ch for i, ch in enumerate(s) if i not in to_remove]
    return "".join(result_chars)


if __name__ == "__main__":
    s = "lee(t(c)o)de)"
    print(minRemoveToMakeValid(s))
