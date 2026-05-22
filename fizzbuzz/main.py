def fizzbuzz_1(n: int) -> list:
    """
    Time: O(n), one constant-time check per integer from 1 to n.
    Space: O(n) for the output list of n strings.
    """
    result = []
    # append = result.append
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
            # append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
            # append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
            # append("Buzz")
        else:
            result.append(str(i))
            # append(str(i))
    return result


def fizzbuzz_2(n: int) -> list:
    """
    Time: O(n), one constant-time check per integer from 1 to n.
    Space: O(n) for the output list of n strings.
    """
    result = []
    # append = result.append
    for i in range(1, n + 1):
        div3 = i % 3 == 0
        div5 = i % 5 == 0

        if div3 and div5:
            result.append("FizzBuzz")
        elif div3:
            result.append("Fizz")
        elif div5:
            result.append("Buzz")
        else:
            result.append(str(i))

    return result


if __name__ == "__main__":
    print(fizzbuzz_2(5))
