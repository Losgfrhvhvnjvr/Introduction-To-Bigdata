# Week 6 — Observations

## Task 1 — A-Priori and association rules

The A-Priori implementation correctly identifies frequent single items
and pairs using the minimum support threshold. In the example dataset,
the rule diaper -> beer has confidence 0.8 and lift approximately 1.12.
All frequent singletons in this small dataset have support 5, so the
two directions of each frequent pair have equal confidence here.
In general, confidence can differ by direction because each rule uses
a different antecedent support.

## Task 2 — Frequent-pair explosion

I tested support thresholds 400, 200, 100, 50, 25, 12, 6, 3 and 1.
As support decreased, the number of frequent pairs rose from 249 to
893,456. Peak counters rose from 10,585 to 893,456, then plateaued
because the algorithm had encountered that many distinct pairs.
The support-1 run completed in 6.96 seconds with 327.1 MB of Python
memory traced; the experiment did not run out of memory.
These memory values come from tracemalloc and do not represent total
system memory. Machine details are recorded in out/explosion.json.

## Task 3 — PCY

With 1,000,003 buckets, PCY found exactly the same 6,397 frequent
pairs as PlainApriori. Peak pair counters fell from 820,259 to 23,356,
a 97.2% reduction. The final benchmark took about 2.11 seconds for
PCY versus 1.69 seconds for the baseline, so fewer counters did not
mean faster execution on this machine.

The bucket-count array uses about 4 MB during pass one. It is released
before pass two, while the bitmap of about 125 KB remains in memory.
These costs matter: PCY does not make the bucket array free. With only
1,009 buckets, the peak pair-counter count rose to 820,259, giving no
reduction. The many collisions made the bitmap filter ineffective.

The crossover depends on the number of candidate pairs avoided, Python's
per-counter memory overhead, the bucket-array size, the support threshold,
and the basket distribution. As a rough estimate, a 4 MB bucket array
may not pay off if it avoids fewer than tens of thousands of Python pair
counter entries; the exact point needs measurements at smaller data sizes.
On this 20,000-basket dataset, avoiding about 797,000 pair counters makes
the trade-off worthwhile in counter memory, though PCY was slightly slower.
