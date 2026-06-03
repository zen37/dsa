Fastest to slowest: **v2 → v3 → v1**

- **v2 `s[::-1]`** — fastest. The entire operation (iterate + build result) runs in C with no Python-level overhead.
- **v3 `"".join(reversed(s))`** — `reversed()` is a lazy C iterator, but `join` still has to call back into Python to collect each character, adding some overhead.
- **v1 manual loop** — slowest. Every iteration (index calculation, `append`) is executed by the Python interpreter.

All three are O(n), so the difference only becomes noticeable on long strings. For typical use the gap is negligible — but if you benchmarked with `timeit`, you'd see roughly this ordering consistently.