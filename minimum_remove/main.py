def minRemoveToMakeValid(s: str) -> str:
    """Remove the minimum number of parentheses so the result is valid."""

    stack: list[int] = []
    to_remove: set[int] = set()
    result: list[str] = []

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()
            else:
                to_remove.add(i)

    to_remove.update(stack)

    for i, ch in enumerate(s):
        if i not in to_remove:
            result.append(ch)

    return "".join(result)


if __name__ == "__main__":
    s = "lee(t(c)o)de)"
    print(minRemoveToMakeValid(s))
