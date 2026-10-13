# Observations — Tasks 1 and 3

## Task 1 — Three streaming sketches

### Bloom Filter

The Bloom filter produced no false negatives. The measured false-positive rate was 0.895%, close to the predicted rate of 0.860%.

### Flajolet-Martin

The estimated number of distinct elements was 11,089, compared with the true count of 19,953. The estimate was within a factor of two of the true count.

### Reservoir Sampling

The uniformity test gave a spread of 8.9%, below the 15% threshold. The test passed.

## Task 3 — Same Memory, Fewer Mistakes

### Parameter and derivation

The parameter changed was the number of hash functions, k.

The optimal value is:

k = (m/n) × ln(2)

With m = 80,000 bits and n = 8,000 items:

k = 10 × ln(2) ≈ 6.93

Therefore, k = 7 was selected.

### Results

The baseline filter produced 19,023 false positives out of 200,000 queries, a rate of 9.511%.

Our filter produced 1,663 false positives, a rate of 0.831%. This represents a 91.3% reduction.

Both filters produced zero false negatives. Our filter used exactly 80,000 bits, respecting the memory budget.

### Theoretical minimum

The theoretical false-positive rate is approximately:

p = (1 - exp(-kn/m))^k

For 10 bits per item and 7 hash functions:

p ≈ (1 - exp(-7 × 8,000 / 80,000))^7

p ≈ (1 - exp(-0.7))^7 ≈ 0.00819 = 0.819%.

The measured rate of 0.831% is very close to the theoretical prediction of 0.819%. The strong grading threshold of 0.9% was reached.

### What if the number of items is unknown?

If the number of items is underestimated, the filter may become too full and its false-positive rate will increase.

If the number is overestimated, more memory than necessary may be allocated.

A scalable Bloom filter can address this problem by adding new filters as the stream grows while controlling the false-positive rate.

## Conclusion

Task 3 reduced the false-positive rate from 9.511% to 0.831%, with zero false negatives and the same 80,000-bit memory budget.
