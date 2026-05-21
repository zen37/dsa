from output import print_anagram_result


def main() -> None:
    """
    Run a few examples.
    """
    print_anagram_result("listen", "silent")  # True
    print_anagram_result("Listen!", "Silent,")  # False
    print_anagram_result("Dirty room", "Dormitory")  # True
    print_anagram_result("hello", "world")  # False
    print_anagram_result("Straße", "StRASSE")  # True with casefold
    print_anagram_result("こんにちは 世界", "世 界 こん にちは")  # True


if __name__ == "__main__":
    main()
