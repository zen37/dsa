# Finding the Lowest Value: Initialization Strategies

When solving problems that require tracking the minimum value seen so far (such as the "Best Time to Buy and Sell Stock" problem), there are two common initialization approaches.

## Option 1: Initialize with the First Element

```python
lowest_price = prices[0]

for price in prices[1:]:
    lowest_price = min(lowest_price, price)
```

### How It Works

- Assume the first element is the lowest value seen so far.
- Start iterating from the second element.
- Update the minimum whenever a smaller value is found.

### Advantages

- Explicit and easy to understand.
- Does not require a special sentinel value.
- Commonly preferred in interviews.

### Considerations

- Requires handling an empty list separately.

```python
if not prices:
    return 0
```

---

## Option 2: Initialize with Infinity

```python
lowest_price = float("inf")

for price in prices:
    lowest_price = min(lowest_price, price)
```

### How It Works

- Start with positive infinity (`∞`).
- Since every real value is less than infinity, the first element automatically becomes the minimum.
- Process all elements using the same logic.

### Advantages

- No need to treat the first element specially.
- Often results in slightly cleaner loops.
- Useful when processing streams of data.

### Considerations

- Uses a sentinel value (`float("inf")`), which may be less intuitive to beginners.

---

## Comparison

| Approach | Empty List Handling | Uses Sentinel Value | Loop Starts At |
|-----------|-------------------|-------------------|----------------|
| First Element | Required | No | Second Element |
| `float("inf")` | Not Required for Minimum Tracking | Yes | First Element |

Both approaches have identical performance characteristics:

- **Time Complexity:** O(n)
- **Space Complexity:** O(1)

---

## Recommendation

For interview problems involving arrays, initializing with the first element is often the most straightforward and readable approach:

```python
lowest_price = prices[0]
```

For more general algorithms where there may not be a natural first value, using:

```python
lowest_price = float("inf")
```

can simplify the implementation.