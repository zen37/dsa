def is_palindrome(s: str) -> bool:
    # Time O(n) + O(n) x O(n) =  O(n power of 2); Space O(n)

    if s == "":
        return True

    s = s.lower()

    alphanumeric_set = {
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    }

    s_new: str = ""

    for char in s:
        if char in alphanumeric_set:
            s_new = s_new + char

    return s_new == s_new[::-1]


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))
    print(is_palindrome("race a car"))
    print(is_palindrome(" "))
    print(is_palindrome("0P"))
    print(is_palindrome("ab_a"))
