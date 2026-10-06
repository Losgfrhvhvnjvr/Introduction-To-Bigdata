# Task 3 — Observation

## LSH parameters

I chose:

- n = 160 hash functions
- b = 80 bands
- r = n / b = 160 / 80 = 2 rows per band

The transition of the S-curve is approximately:

(1 / b)^(1 / r)

= (1 / 80)^(1 / 2)

≈ 0.112

This is well below the similarity threshold of 0.6. I chose this
configuration to favor recall and avoid missing truly similar pairs.

## Results

With 2,120 documents and a threshold of 0.6:

- Comparisons: 61,362
- Recall: 95.9%
- Precision: 100.0%
- Comparisons avoided: 97.27%

The brute-force baseline makes 2,246,140 comparisons.

The LSH method therefore makes far fewer comparisons while still
finding 95.9% of the truly similar pairs.

## Changing the parameters

With 120 hashes and 40 bands, I obtained:

- Recall: 90.1%
- Comparisons avoided: 99.35%

With 120 hashes and 60 bands:

- Recall: 93.4%
- Comparisons avoided: 98.99%

Increasing the number of bands increased recall, but also increased
the number of candidate pairs.

The final configuration (160 hashes, 80 bands) gave a recall of 95.9%.
It therefore gives a better recall, although it avoids fewer comparisons.

## When is hashing no longer free?

The harness does not count the cost of computing MinHash signatures
and LSH buckets. This is a reasonable simplification when the cost of
comparing two large documents is much higher than the cost of hashing
them.

At a very small number of documents, however, the hashing overhead can
become significant because brute force is already fast. At a very large
scale, hashing can also require significant CPU time and memory, so it
would no longer be reasonable to consider it completely free.