# `longest_common_prefix` — Benchmark Results

Median time per call across four implementations (`dict`, `vscan`, `zip`, `column`).
Settings: `repeats=10`, `number=5`, reporting median per call. All times in microseconds (µs).

## n = 200 strings, m = 200 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 7401.7 | 1068.3 | 264.3 | 1124.2 |
| no_match (exit at 0) | 7464.3 | 3.0 | 5.2 | 0.5 |
| late_mismatch (exit at m-1) | 7434.5 | 1073.2 | 264.2 | 1023.7 |
| one_short_string | 7407.0 | 13.6 | 7.3 | 17.3 |

## n = 200 strings, m = 10 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 376.2 | 56.2 | 17.4 | 56.6 |
| no_match (exit at 0) | 358.2 | 3.0 | 5.2 | 0.5 |
| late_mismatch (exit at m-1) | 368.0 | 51.5 | 16.9 | 46.8 |
| one_short_string | 388.7 | 13.5 | 7.6 | 18.0 |

## n = 10 strings, m = 200 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 396.8 | 82.5 | 32.5 | 58.2 |
| no_match (exit at 0) | 379.7 | 0.6 | 0.5 | 0.2 |
| late_mismatch (exit at m-1) | 394.3 | 82.0 | 32.6 | 57.5 |
| one_short_string | 340.8 | 1.3 | 0.7 | 1.1 |

## n = 2 strings, m = 200 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 97.5 | 38.6 | 22.1 | 16.9 |
| no_match (exit at 0) | 77.9 | 0.5 | 0.3 | 0.2 |
| late_mismatch (exit at m-1) | 96.2 | 38.6 | 22.0 | 16.9 |
| one_short_string | 40.4 | 0.7 | 0.4 | 0.4 |

## n = 2000 strings, m = 50 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 18703.3 | 2624.5 | 671.2 | 2780.1 |
| no_match (exit at 0) | 19254.8 | 25.1 | 52.3 | 3.8 |
| late_mismatch (exit at m-1) | 19386.7 | 2641.7 | 720.6 | 2554.9 |
| one_short_string | 18478.6 | 129.0 | 69.7 | 167.2 |

## n = 20000 strings, m = 50 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 186161.7 | 26170.5 | 6824.6 | 27989.8 |
| no_match (exit at 0) | 192229.1 | 246.0 | 523.1 | 48.5 |
| late_mismatch (exit at m-1) | 188824.0 | 26075.6 | 7053.0 | 26023.2 |
| one_short_string | 191806.9 | 1283.1 | 707.6 | 1668.4 |

## n = 100000 strings, m = 50 chars

| Workload | dict | vscan | zip | column |
|---|---:|---:|---:|---:|
| full_match (prefix = m) | 962182.0 | 130305.0 | 34622.7 | 138791.9 |
| no_match (exit at 0) | 946285.4 | 1237.9 | 3009.7 | 226.4 |
| late_mismatch (exit at m-1) | 948921.9 | 134606.0 | 36827.8 | 134186.9 |
| one_short_string | 932068.1 | 6434.3 | 3772.0 | 8361.7 |