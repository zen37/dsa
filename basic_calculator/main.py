def calculate(s: str) -> int:

    result: int = 0
    num: int = 0
    sign: int = 1
    stack: list[tuple[int, int]] = []

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
            previous_result = result
            result = 0
            previous_sign = sign
            sign = 1
            stack.append([previous_result, previous_sign])
        elif ch == ")":
            result += num * sign
            previous_result, previous_sign = stack.pop()
            result = previous_result + result * previous_sign
            sign = 1
            num = 0

    result += num * sign

    return result


if __name__ == "__main__":
    print(calculate("1 - 3 - (1 + 1) + 1"))
