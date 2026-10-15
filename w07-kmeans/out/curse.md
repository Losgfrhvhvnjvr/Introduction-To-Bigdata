# Week 7 — Task 2: Curse of dimensionality

## Measurements

| Dimension | Points | Pairs | Mean | Min | Max | Contrast | Relative SD | Seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 200 | 19897 | 1.8161 | 0.9460 | 2.6363 | 1.7868 | 0.1312 | 0.06 |
| 2 | 1000 | 19978 | 0.5210 | 0.0027 | 1.3255 | 488.5816 | 0.4759 | 0.02 |
| 2 | 1000 | 19978 | 0.5210 | 0.0027 | 1.3255 | 488.5816 | 0.4759 | 0.02 |
| 5 | 1000 | 19977 | 0.8842 | 0.1106 | 1.6874 | 14.2566 | 0.2816 | 0.03 |
| 5 | 1000 | 19977 | 0.8842 | 0.1106 | 1.6874 | 14.2566 | 0.2816 | 0.03 |
| 10 | 1000 | 19977 | 1.2735 | 0.4385 | 2.1595 | 3.9252 | 0.1927 | 0.04 |
| 10 | 1000 | 19977 | 1.2735 | 0.4385 | 2.1595 | 3.9252 | 0.1927 | 0.04 |
| 20 | 1000 | 19981 | 1.8153 | 0.8208 | 2.6699 | 2.2527 | 0.1352 | 0.06 |
| 20 | 1000 | 19981 | 1.8153 | 0.8208 | 2.6699 | 2.2527 | 0.1352 | 0.07 |
| 20 | 1000 | 19981 | 1.8153 | 0.8208 | 2.6699 | 2.2527 | 0.1352 | 0.06 |
| 50 | 1000 | 19977 | 2.8673 | 1.9092 | 3.7849 | 0.9824 | 0.0830 | 0.11 |
| 50 | 1000 | 19977 | 2.8673 | 1.9092 | 3.7849 | 0.9824 | 0.0830 | 0.14 |
| 100 | 1000 | 19974 | 4.0681 | 3.2057 | 4.9535 | 0.5452 | 0.0598 | 0.22 |
| 100 | 1000 | 19974 | 4.0681 | 3.2057 | 4.9535 | 0.5452 | 0.0598 | 0.23 |
| 200 | 1000 | 19980 | 5.7761 | 4.8709 | 6.6818 | 0.3718 | 0.0414 | 0.42 |
| 200 | 1000 | 19980 | 5.7761 | 4.8709 | 6.6818 | 0.3718 | 0.0414 | 0.40 |
| 20 | 2000 | 19989 | 1.8177 | 0.8208 | 2.8304 | 2.4483 | 0.1337 | 0.06 |
| 500 | 2000 | 19983 | 9.1262 | 8.0991 | 10.1758 | 0.2564 | 0.0264 | 1.09 |
| 1000 | 2000 | 19997 | 12.9087 | 11.9705 | 13.8064 | 0.1534 | 0.0186 | 2.06 |

## A3 — Contrast thresholds

- Contrast first falls below 1.0 at dimension 50 (contrast 0.9824).
- Contrast first falls below 0.5 at dimension 200 (contrast 0.3718).

## A4 — Mean distance

For uniformly distributed points in a unit cube, the mean Euclidean distance is expected to grow approximately as the square root of dimension, rather than linearly. The mean/sqrt(d) ratios below help assess this trend:

| Dimension | Mean | Mean / sqrt(d) |
|---:|---:|---:|
| 2 | 0.5210 | 0.3684 |
| 2 | 0.5210 | 0.3684 |
| 5 | 0.8842 | 0.3954 |
| 5 | 0.8842 | 0.3954 |
| 10 | 1.2735 | 0.4027 |
| 10 | 1.2735 | 0.4027 |
| 20 | 1.8153 | 0.4059 |
| 20 | 1.8153 | 0.4059 |
| 20 | 1.8153 | 0.4059 |
| 50 | 2.8673 | 0.4055 |
| 50 | 2.8673 | 0.4055 |
| 100 | 4.0681 | 0.4068 |
| 100 | 4.0681 | 0.4068 |
| 200 | 5.7761 | 0.4084 |
| 200 | 5.7761 | 0.4084 |

## A5 — Relative standard deviation

- Dimension 2: relative SD = 0.4759.
- Dimension 2: relative SD = 0.4759.
- Dimension 5: relative SD = 0.2816.
- Dimension 5: relative SD = 0.2816.
- Dimension 10: relative SD = 0.1927.
- Dimension 10: relative SD = 0.1927.
- Dimension 20: relative SD = 0.1352.
- Dimension 20: relative SD = 0.1352.
- Dimension 20: relative SD = 0.1352.
- Dimension 50: relative SD = 0.0830.
- Dimension 50: relative SD = 0.0830.
- Dimension 100: relative SD = 0.0598.
- Dimension 100: relative SD = 0.0598.
- Dimension 200: relative SD = 0.0414.
- Dimension 200: relative SD = 0.0414.

Contrast uses the two extreme sampled distances and is sensitive to sample size. Relative SD measures the overall dispersion relative to the mean, so it often gives a more stable picture of distance concentration.

## A6 — Effect of point count

At dimension 20, the observed contrast changes with point count:

- 200 points: contrast = 1.7868, min = 0.9460, max = 2.6363.
- 1000 points: contrast = 2.2527, min = 0.8208, max = 2.6699.
- 1000 points: contrast = 2.2527, min = 0.8208, max = 2.6699.
- 1000 points: contrast = 2.2527, min = 0.8208, max = 2.6699.
- 2000 points: contrast = 2.4483, min = 0.8208, max = 2.8304.

The minimum and maximum are sample extremes, so their gap can change as the number of sampled points increases. The random sampling also introduces variation between runs.

## A7 — Machine and runtime

- Platform: Windows-11-10.0.26200-SP0
- Processor: Intel64 Family 6 Model 154 Stepping 4, GenuineIntel
- Python: 3.13.15
- Longest recorded measurement: dimension 1000, 2000 points, 2.06 seconds.

## A8 — Connection to Week 3 LSH

These results do not automatically invalidate LSH from Week 3. This experiment measures Euclidean distances between uniformly distributed points in a unit cube, whereas the Week 3 method uses Jaccard similarity on shingle sets. The distance metric and data distribution are different. LSH performance must be evaluated for the relevant similarity measure and dataset.
