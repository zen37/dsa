# Minimum Remove to Make Valid Parentheses

## Instructions

The problem: Given a string `s` of `'('`, `')'`, and lowercase English letters,
remove the minimum number of parentheses (any positions) so that the
resulting string is valid, and return any valid result. A string is valid if
it is empty, or it is a valid string surrounded by `(...)`, or it is a
concatenation of valid strings. Letters are always kept.

### Examples

```
Input:  "lee(t(c)o)de)"   Output: "lee(t(c)o)de"   (remove the last ')')
Input:  "a)b(c)d"         Output: "ab(c)d"
Input:  "))(("            Output: ""
Input:  "(a(b(c)d)"       Output: "a(b(c)d)"   (one '(' removed)
```

In principle some inputs have more than one minimal valid answer (for
`"(a(b(c)d)"` both `"a(b(c)d)"` and `"(ab(c)d)"` are valid and remove exactly
one `'('`). The tests below expect the result produced by the index-stack
approach this scaffold teaches: push the index of every `'('`, drop unmatched
`')'` as you meet them, and at the end drop whatever `'('` indices are still
on the stack. Follow that recipe and your output will match.

### Pre-flight checklist

Answer all four in your submission before you code:

1. Name the pattern in one sentence. How is this the same stack invariant as
   Valid Parentheses, and what changes (you are not returning a bool, you are
   deciding which indices to delete)?
2. Target complexity: state your time and space in terms of `N = len(s)`, and
   why.
3. Approach: how do you use the stack to identify the exact indices to
   remove? Be specific about what you push and what is left over at the end.
4. Edge or failure case: name one input that a too-simple approach (e.g. just
   deleting the first/last bad bracket) gets wrong, and how your approach
   handles it.

## Pre-flight answers

**1. Name the pattern.**

This is the **same LIFO invariant as Valid Parentheses**: the stack always holds exactly the currently *unmatched* opens, with the innermost (most recent) on top, so any close can only ever validly pair with the top. What changes is the *output*: Valid Parentheses only asks "is the stack empty at the end?" (a yes/no verdict), whereas here you need to know **which specific characters** caused the failure, so instead of pushing the bracket character itself, you push its **index** — giving you a way to mark, and later delete, the exact positions that never found a match.

**2. Target complexity.**

**Time: O(N).** One left-to-right pass to scan and build the stack, plus one more pass at the end to build the result while skipping marked indices — both O(N), so O(N) total.

**Space: O(N).** The stack can hold up to N indices in the worst case (a string of all `'('`, e.g. `"((((("`), and the removal-marker structure (a set, or a boolean array) is also O(N), sized to the string length.

**3. Approach.**

Scan left to right, tracking indices, not characters:
- On `'('`: push its **index** onto the stack.
- On `')'`: if the stack is non-empty, **pop** (that `(` found its match — nothing to remove). If the stack **is** empty, this `)` has no opener to pair with, so mark **this index** for removal right now.
- On a letter: do nothing (always kept).

At the end, whatever indices are **still on the stack** are `'('` characters that never got matched — mark all of those for removal too.

Finally, build the result by walking the string once more, including every character **except** those at the marked (removed) indices.

So: the stack tells you which `(` were never closed (leftover at the end), and an immediate check tells you which `)` never had an opener (found the instant the stack is empty when a `)` arrives). Together those two sets of indices are exactly, and only, the minimum characters that must be deleted.

**4. Edge/failure case.**

`"()())"` — a too-simple approach that just "removes the first bad bracket it finds" or "removes the last character" would likely delete the final `)` and stop, assuming one deletion fixes everything reflexively at the end — and it happens to work *here*, `"()()"`  is valid... but consider `"(()"`: a naive "delete the last unmatched thing you notice" approach might delete the wrong `(` or miscount, especially on something like `"())("` — here a naive "just remove the last bad bracket" fails because there are unmatched brackets at **both ends** (an extra `)` early on *and* an extra `(` at the end), and a rule that only looks at one side (e.g. "trim trailing invalid characters") misses the other. My approach handles this correctly because it separately tracks: (a) `)` with no opener — caught immediately, mid-scan, via the empty-stack check; and (b) `(` with no closer — caught at the end, via leftover stack contents. Both failure modes are detected independently and precisely by index, regardless of where in the string they occur, so mixed front-and-back invalidity like `"())("` is handled correctly, unlike a rule that only trims one end.