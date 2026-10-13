# Task 2 — Limits of Exact Distinct Counting

## Objective

This experiment compares exact distinct counting using a Python set with the Flajolet-Martin sketch. The stream contains approximately 40% distinct items.

## Measurements

| Stream size | Exact distinct count | Exact time | Exact peak memory | FM ratio | FM time | FM peak memory |
|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 0.31 s | 3.9 MB | 0.86x | 7.75 s | 0.00 MB |
| 400,000 | 146,970 | 1.15 s | 11.6 MB | 0.60x | 30.61 s | 0.00 MB |
| 1,600,000 | 587,625 | 4.75 s | 46.6 MB | 0.78x | 125.44 s | 0.00 MB |
| 6,400,000 | 2,349,909 | 20.49 s | 188.3 MB | 0.60x | 628.30 s | 0.00 MB |
| 12,800,000 | 4,699,458 | 90.48 s | 377.6 MB | Not measured | Not measured | Not measured |

## Discussion

Exact counting became slower and required more memory as the stream size increased. At 6.4 million items, it took 20.49 seconds and used 188.3 MB of peak memory. At 12.8 million items, exact counting took 90.48 seconds and used 377.6 MB.

Flajolet-Martin took 628.30 seconds (about 10 minutes 28 seconds) at 6.4 million items. Its reported peak memory was 0.00 MB after rounding; this does not mean it uses literally no memory. The sketch is designed to use a small amount of memory compared with storing every distinct item in a set.

The Flajolet-Martin estimate ratios ranged from 0.60x to 0.86x. All measurements remained within a factor of two of the exact count, although the estimates were lower than the actual counts.

## Conclusion

Exact counting remained possible at 12.8 million items, but it took about 90.5 seconds and used 377.6 MB of peak memory. The point where exact counting becomes unbearable has not yet been reached conclusively.

The current Flajolet-Martin implementation was much slower than exact counting in these experiments. Therefore, these measurements demonstrate its memory advantage more clearly than a runtime advantage. The 12.8-million-item experiment measured exact counting only; Flajolet-Martin was not measured at that size.

## Reproducibility

Command used for the main comparison:

`py -3.13 task2_limits.py --sizes 100000,400000,1600000,6400000`

An additional exact-counting measurement was performed at 12,800,000 items.

Raw measurements are stored in `out/limits.json`.

## Machine specifications

- **Operating system:** Windows 11 (build 26200)
- **Processor:** Intel64 Family 6 Model 154 Stepping 4 (GenuineIntel)
- **Python:** 3.13.15