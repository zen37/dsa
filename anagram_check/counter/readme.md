**Memory: Counter uses more, guaranteed.**

Two count tables instead of one. Same Big-O class (`O(k)` either way), but the constant factor is ~2× because both tables exist simultaneously in memory until the comparison finishes.

**Speed: Counter is usually faster, but "usually" not "always".**

Why it's usually faster:
- The counting loop runs entirely in C, no per-character bytecode dispatch.
- `dict` equality (`==`) is also C — it short-circuits on the first mismatch.

When the hand-rolled version could win:
- Very short strings where the C-loop startup overhead dominates.
- Cases where the strings differ early — your hand-rolled version returns `False` after seeing the first mismatched character in `s2`, while `Counter` always reads all of `s1` *and* all of `s2` before comparing. On a worst case like `"a" + "x" * 1_000_000` vs `"b" + "x" * 1_000_000`, the hand-rolled one bails almost instantly; `Counter` still builds both tables first.

So the real trade-off is:

| | Memory | Speed (typical) | Speed (early-mismatch) |
|---|---|---|---|
| Hand-rolled | lower | slower | **much faster** |
| `Counter` | higher | **faster** | slower |

For most realistic inputs, `Counter` wins. For pathological adversarial inputs where mismatches happen at character 1 of a huge string, the hand-rolled version wins. Big-O hides all of this.