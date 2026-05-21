# Python Style Guide Cheat Sheet

## 1. Core Principle: Write for the Reader

Optimize for clarity over cleverness. Data Structures and Algorithms coding questions are already concept-heavy; unclear style adds unnecessary difficulty. Simple, readable, easy-to-review code makes it easier for you and your interviewer to follow along.

```python
# Prefer this: explicit and easy to reason about
seen = set()

for num in nums:
    if num in seen:
        return True
    seen.add(num)

return False
```

```python
# Avoid this: clever, but hides the algorithm
return len(nums) != len(set(nums))
```

## 2. Naming: Make Meaning Obvious

### 2.1 Variables

Use `snake_case` and choose names that describe purpose. Readers should understand intent without decoding abbreviations.

```python
# Avoid this: short or unclear names
tc = 0
n = len(nodes)
flag = False
```

```python
# Prefer this: clear intent
total_cost = 0
node_count = len(nodes)
is_visited = False
```

### 2.2 Collections and Loop Variables

Use plural names for collections and singular names for single elements. Plural names make the type and role of a variable obvious at a glance.

This helps prevent common beginner DSA mistakes such as:

- Treating a collection like a single value
- Misreading loop logic because collection and item names are confusing
- Confusing a node with its neighbors

```python
# Avoid this: ambiguous
value = [1, 2, 3]
visit = set()

for value in value:
    ...
```

```python
# Prefer this: clear intent
values = [1, 2, 3]
visited = set()

for value in values:
    ...
```

Use short loop names like `i` and `j` only in tight numeric loops.

```python
for i in range(len(nums)):
    ...
```

Use descriptive names when meaning matters.

```python
for neighbor in graph[node]:
    ...
```

### 2.3 Functions, Classes, and Constants

Name things based on what they do and what they represent.

Functions and methods use `snake_case` verbs. Functions perform actions, so their names should describe behavior.

```python
def build_prefix_table(pattern: str) -> list[int]:
    ...


def compute_distance(a: int, b: int) -> int:
    ...
```

Classes use `PascalCase` nouns. Classes represent objects or concepts.

```python
class Thermostat:
    ...


class TreeNode:
    ...
```

Constants use `UPPER_SNAKE_CASE`. This signals values that should not change.

```python
INF = 10**18
DEFAULT_CAPACITY = 16
```

## 3. Formatting: PEP 8 Essentials

Use 4 spaces for indentation. Use spaces around operators and after commas. Wrap long lines.

```python
mid = (lo + hi) // 2

result = some_function(
    first_argument,
    second_argument,
)
```

## 4. Comments: Explain Why, Not What

Comments should explain intent or tricky reasoning, not obvious steps.

```python
# Maintain a sliding window with at most k distinct values
while right < n:
    ...
```

```python
# Avoid this: the code already says this
# Increment right
right += 1
```

## 5. Functions: Small and Focused

Each function should do one thing and do it clearly. Smaller functions are easier to read, test, reuse, and debug. If a function mixes setup, algorithm logic, formatting, and other responsibilities, split it into helpers.

```python
def build_adj_list(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    ...


def bfs_order(graph: list[list[int]], start: int) -> list[int]:
    ...
```

## 6. Type Hints: Required

Always type-hint function parameters and return values. Use built-in generics such as `list[int]` and `dict[str, int]`.

```python
def bfs(graph: list[list[int]], start: int) -> list[int]:
    ...
```

Use `| None` when `None` is a valid value.

```python
def find_node(root: Node, key: int) -> Node | None:
    ...
```

## 7. Mutability and Safety

Never use mutable default arguments such as `[]`, `{}`, or `set()`. Default values are created once when the function is defined, so the same object gets reused across calls. This can cause hard-to-debug “ghost data” bugs.

```python
# Avoid this: the same list is reused every call
def add_edge(edges=[]):
    edges.append((0, 1))
    return edges
```

```python
# Prefer this: create a new list when needed
def add_edge(edges: list[tuple[int, int]] | None = None) -> list[tuple[int, int]]:
    if edges is None:
        edges = []

    edges.append((0, 1))
    return edges
```

Validate inputs and fail early. DSA solutions often rely on assumptions such as sorted input, valid indices, or non-empty lists. Checking early prevents confusing downstream errors and makes bugs obvious.

```python
def kth_smallest(nums: list[int], k: int) -> int | None:
    if not nums:
        return None

    ...
```

## 8. Complexity Notes: Required

Include Big-O time and space complexity for major functions.

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    # Time: O(n), Space: O(n)
    ...
```
