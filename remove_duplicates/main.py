def remove_duplicates(lst: list) -> list:
    # Time: O(n), Space: O(n)

    unique_items = {}

    for item in lst:
        unique_items[item] = None

    return list(unique_items.keys())


if __name__ == "__main__":
    lst = []
    print(remove_duplicates(lst))
