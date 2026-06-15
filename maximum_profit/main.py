def max_profit(prices: list[int]) -> int:

    # Time complexity: O(n) - We traverse the list of prices once.
    # Space complexity: O(1) - We use a constant amount of space for variables

    if len(prices) <= 1:
        return 0

    lowest_price: int = prices[0]
    profit: int = 0
    max_profit: int = 0

    for i in range(1, len(prices)):
        # print(
        if prices[i] < lowest_price:
            lowest_price = prices[i]

        profit = prices[i] - lowest_price

        if max_profit < profit:
            max_profit = profit

    return max_profit


if __name__ == "__main__":
    print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 5
    print(max_profit([7, 6, 4, 3, 1]))  # Output: 0
    print(max_profit([1, 2, 3, 4, 5]))  # Output: 4
    print(max_profit([2, 10, 1, 15]))  # Output: 14
