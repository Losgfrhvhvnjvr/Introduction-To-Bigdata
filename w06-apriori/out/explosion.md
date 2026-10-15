# Task 2 — Frequent-pair explosion

## A2 — Where the experiment became unbearable

The experiment did not become unbearable on this machine.
The lowest tested support was 1. The run completed in 6.96 seconds
with 893,456 frequent pairs and 327.1 MB of Python memory traced.
No memory exhaustion or execution failure was observed.

## Measurements

| Support | Frequent pairs | Peak pair counters | Time (s) | Python peak memory (MB) |
|---:|---:|---:|---:|---:|
| 400 | 249 | 10,585 | 0.76 | 1.1 |
| 200 | 776 | 58,626 | 1.15 | 6.4 |
| 100 | 2,244 | 273,701 | 2.45 | 26.4 |
| 50 | 6,397 | 820,259 | 5.65 | 102.2 |
| 25 | 17,045 | 893,456 | 6.20 | 102.2 |
| 12 | 43,116 | 893,456 | 4.69 | 102.8 |
| 6 | 101,938 | 893,456 | 5.18 | 119.4 |
| 3 | 250,054 | 893,456 | 5.06 | 156.7 |
| 1 | 893,456 | 893,456 | 6.96 | 327.1 |

## A4 — Counter growth as support falls

The number of counters did not grow linearly with decreasing support.
When support was halved from 400 to 200, counters increased by about
5.54 times; from 200 to 100, by 4.67 times; and from 100 to 50,
by 3.00 times. From support 50 to 25, growth slowed to about 1.09 times.
The counter count then plateaued at 893,456 because the algorithm had
encountered that many distinct pairs in these baskets.

From support 400 to support 1, the peak counter count increased by
about 84 times.

## A5 — Frequent answers versus counters

Frequent pairs increased from 249 at support 400 to 893,456 at support 1,
about 3,588 times as many. Peak counters increased about 84 times.
At support 1, every distinct pair encountered is frequent because each
has appeared at least once.

The number of answers and the work needed to discover them behave
differently. Lowering the threshold admits many more pairs, while the
algorithm may already be holding counters for nearly every distinct pair
it encounters. This gap motivates PCY, which filters candidate pairs
before counting them individually.

## A6 — Machine and environment

- CPU: 12th Gen Intel(R) Core(TM) i7-1255U
- Installed RAM: approximately 15.7 GB (about 16 GB)
- Operating system: Windows (platform details recorded in explosion.json)
- Python: 3.13
- Other applications running during the experiment: VS Code, Google Chrome

Note: memory values above are Python memory traced by tracemalloc, not
the total memory used by the entire operating system process.
