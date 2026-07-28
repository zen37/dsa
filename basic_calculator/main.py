def calculate(s: str) -> int:

    stack: list[tuple[int, int]] = []
    result: int = 0
    sign: int = 1
    num: int = 0

    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)

        elif ch in "+-":
            result += num * sign
            num = 0
            if ch == "+":
                sign = 1
            else:
                sign = -1

    result += num * sign
    return result


if __name__ == "__main__":
    print(calculate("1231 + 3"))
