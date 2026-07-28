```markdown
# Problem Statement

**Problem:**
Given a string `s` representing a valid expression with non-negative integers, `+`, `-`, `(`, `)`, and spaces, evaluate it and return its value. There is no `*` or `/` in this variant, but there **are** parentheses and unary-style signs, which is the new hard part.

---

## Examples

| Input                     | Output |
|---------------------------|--------|
| `"1 + 1"`                 | 2      |
| `" 2-1 + 2 "`             | 3      |
| `"(1+(4+5+2)-3)+(6+8)"`   | 23     |

---

## Pre-flight Checklist

### 1. Pattern Identification
**Name the pattern in one sentence:**
The problem involves evaluating a mathematical expression with parentheses and unary signs, requiring context management for nested sub-expressions.

---

### 2. Stack Usage
**What is the stack actually storing when you hit a `(`?**
The stack stores the **current result** and the **current sign** before encountering the `(` to restore the context after evaluating the sub-expression inside the parentheses.

---

### 3. Time and Space Complexity
**Target time and space complexity in terms of `n` (length of `s`):**
- **Time Complexity:** O(n) — We process each character in the string exactly once.
- **Space Complexity:** O(n) — In the worst case (e.g., deeply nested parentheses), the stack could store up to O(n) elements.

**Why?**
The algorithm processes each character once, and the stack depth is proportional to the maximum nesting level of parentheses.

---

### 4. Approach
**How do you track the running result and the current sign, and what exactly do you push on `(` and pop on `)`?**

- **Tracking Running Result and Sign:**
  - Maintain a `result` variable to accumulate the running total.
  - Use a `sign` variable (initially `+1`) to track the current sign (`+1` for `+`, `-1` for `-`).
  - Use a `num` variable to build multi-digit numbers from the string.

- **On `(`:**
  - Push the current `result` and `sign` onto the stack.
  - Reset `result` to `0` and `sign` to `+1` to start evaluating the sub-expression inside the parentheses.

- **On `)`:**
  - Pop the stack to retrieve the **saved result** and **saved sign**.
  - Combine the sub-expression result (`result`) with the saved result using the saved sign:
    `result = saved_result + (saved_sign * result)`
  - Reset `result` to this new value.

---
### 5. Edge Case
**Name one edge or failure case you will test:**
**Input:** `"-(3-4)"`
**Correct Answer:** `1`

**Explanation:**
The unary `-` before the `(` applies to the entire sub-expression `(3-4)`, which evaluates to `-1`. The outer `-` flips the sign, resulting in `1`.

---
## Anchor: Save-and-Restore Context
Use the following approach:
1. **Keep** `result`, `num`, and `sign`.
2. **On `(`:**
   - Push `result` and `sign` onto the stack.
   - Reset `result` to `0` and `sign` to `+1`.
3. **On `)`:**
   - Pop the stack to retrieve the saved `result` and `sign`.
   - Fold the sub-expression result into the saved context:
     `result = saved_result + (saved_sign * result)`
4. **No `*` or `/`:** Precedence is not needed; only sign propagation across parentheses is required.
```