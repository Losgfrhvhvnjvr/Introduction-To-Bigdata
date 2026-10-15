#!/usr/bin/env python3
"""Week 6 · Task 3 — Make pass two fit.

Textbook §6.3 (PCY), §6.3.2 - §6.3.4.

`PlainApriori` does what Task 1 asked: use pass one to drop infrequent items,
then count every pair of surviving items. That is already much better than
counting all pairs. It is still not enough, because the surviving items are the
common ones, and the common ones appear together constantly.

The harness measures **the peak number of pair counters you held**, because
that is the thing that decides whether the algorithm runs at all. §6.3 is about
spending pass one's spare memory to shrink it.

    python3 bench.py
    python3 bench.py --yours

Correctness first: you must find exactly the same frequent pairs. Finding fewer
is not an optimisation.
"""
from collections import Counter
from itertools import combinations


class PlainApriori:
    """Pass one drops infrequent items. Pass two counts every surviving pair."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()
        for basket in baskets:
            counts.update(basket)
        frequent = {i for i, c in counts.items() if c >= self.support}

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(basket & frequent)
            for pair in combinations(items, 2):
                pair_counts[pair] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}



class YourAlgorithm:
    """PCY: use bucket counts in pass one to filter pair candidates."""

    BUCKET_COUNT = 1_000_003

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    @staticmethod
    def bucket(pair):
        # The pair must be sorted so both passes use the same bucket.
        return hash((pair[0], pair[1])) % YourAlgorithm.BUCKET_COUNT

    def run(self, baskets):
        from array import array
        from collections import Counter
        from itertools import combinations

        # Pass 1: count individual items and hashed pairs.
        item_counts = Counter()
        bucket_counts = array('I', [0]) * self.BUCKET_COUNT

        for basket in baskets:
            item_counts.update(basket)
            items = sorted(basket)
            for pair in combinations(items, 2):
                bucket_counts[self.bucket(pair)] += 1

        frequent_items = {
            item for item, count in item_counts.items()
            if count >= self.support
        }

        # Convert bucket counts to a compact bitmap.
        bitmap = bytearray((self.BUCKET_COUNT + 7) // 8)
        for i, count in enumerate(bucket_counts):
            if count >= self.support:
                bitmap[i >> 3] |= 1 << (i & 7)

        # Release the bucket-count array before creating pair counters.
        del bucket_counts
        del item_counts

        # Pass 2: count only pairs passing the PCY bitmap filter.
        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent_items)
            for pair in combinations(items, 2):
                bucket = self.bucket(pair)
                if bitmap[bucket >> 3] & (1 << (bucket & 7)):
                    pair_counts[pair] += 1

            self.peak_counters = max(
                self.peak_counters, len(pair_counts)
            )

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= self.support
        }

