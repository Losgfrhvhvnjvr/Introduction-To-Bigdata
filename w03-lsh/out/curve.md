# Task 2 — Crossover observation

The measurements were performed on my machine for increasing numbers
of documents.

| Documents | Brute-force time | Brute comparisons | LSH time | LSH comparisons |
|---:|---:|---:|---:|---:|
| 250 | 0.20 s | 31,125 | 2.82 s | 370 |
| 500 | 0.81 s | 124,750 | 5.30 s | 2,536 |
| 1000 | 3.74 s | 499,500 | 11.08 s | 12,566 |
| 2000 | 14.54 s | 1,999,000 | 22.82 s | 54,716 |
| 4000 | 16.94 s | 2,246,140 | 23.62 s | 61,362 |
| 8000 | 15.95 s | 2,246,140 | 23.65 s | 61,362 |

The LSH method makes far fewer similarity comparisons, but on this
machine its hashing and bucketing overhead is still larger than the
saved comparison time for this dataset.

The dataset contains only 2,120 documents, so the 4,000 and 8,000
requests use all available documents rather than creating larger
datasets.