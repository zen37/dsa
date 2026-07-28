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

        elif ch == "(":
            stack.append([result, sign])
            result = 0
            sign = 1

        elif ch == ")":
            result += num * sign
            result_previous, sign_previous = stack.pop()
            result = result * sign_previous + result_previous
            num = 0
            sign = 1

    result += num * sign
    return result


if __name__ == "__main__":
    print(calculate("1 - 3 - (1 + 1) + 99"))
