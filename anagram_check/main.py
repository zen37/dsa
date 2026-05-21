from argparse import ArgumentParser, Namespace

from output import print_anagram_result


def build_parser() -> ArgumentParser:
    """
    Build the command-line argument parser.
    """
    parser = ArgumentParser(description="Check whether two strings are anagrams.")

    parser.add_argument("s1", nargs="?", help="first string to compare")
    parser.add_argument("s2", nargs="?", help="second string to compare")
    parser.add_argument(
        "--show-full-text",
        action="store_true",
        help="print complete strings instead of truncating long output",
    )
    parser.add_argument(
        "--more-text",
        type=int,
        default=0,
        metavar="CHARS",
        help="show this many extra characters beyond the configured display length",
    )

    return parser


def run_examples(*, show_full_text: bool = False, more_text: int = 0) -> None:
    """
    Run a few examples.
    """
    print_anagram_result(
        "listen",
        "silent",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # True
    print_anagram_result(
        "Listen!",
        "Silent,",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # False
    print_anagram_result(
        "Dirty room",
        "Dormitory",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # True
    print_anagram_result(
        "hello",
        "world",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # False
    print_anagram_result(
        "Straße",
        "StRASSE",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # True with casefold,  # False without casefold
    print_anagram_result(
        "こんにちは 世界",
        "世 界 こん にちは",
        show_full_text=show_full_text,
        more_text=more_text,
    )  # True


def main() -> None:
    """
    Run examples or compare two strings from command-line arguments.
    """
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()

    if args.more_text < 0:
        parser.error("--more-text must be 0 or greater")

    if args.s1 is None and args.s2 is None:
        run_examples(show_full_text=args.show_full_text, more_text=args.more_text)
        return

    if args.s1 is None or args.s2 is None:
        parser.error("provide both s1 and s2, or neither to run examples")

    print_anagram_result(
        args.s1,
        args.s2,
        show_full_text=args.show_full_text,
        more_text=args.more_text,
    )


if __name__ == "__main__":
    main()
