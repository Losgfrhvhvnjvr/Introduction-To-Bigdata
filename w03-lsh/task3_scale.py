#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """LSH-based near-duplicate finder."""

    def __init__(self, threshold):
        self.threshold = threshold

        # LSH parameters
        self.n_hashes = 160
        self.bands = 80
        self.rows_per_band = self.n_hashes // self.bands

    def find(self, docs, similarity):
        """Return similar document pairs using MinHash + LSH."""

        if len(docs) < 2:
            return set()

        # Give every shingle an integer ID
        shingle_ids = {}
        for doc in docs:
            for shingle in doc:
                if shingle not in shingle_ids:
                    shingle_ids[shingle] = len(shingle_ids)

        n_rows = len(shingle_ids)

        if n_rows == 0:
            return set()

        # Hash functions: h(x) = (a*x + b) mod prime
        prime = 1000003

        hashes = []
        for k in range(self.n_hashes):
            a = 2 * k + 1
            b = k * 17 + 1

            def h(x, a=a, b=b):
                return (a * x + b) % prime

            hashes.append(h)

        # MinHash signatures
        signatures = []

        for doc in docs:
            signature = [prime] * self.n_hashes

            for shingle in doc:
                row = shingle_ids[shingle]

                for k, h in enumerate(hashes):
                    value = h(row)
                    if value < signature[k]:
                        signature[k] = value

            signatures.append(signature)

        # LSH: find candidate pairs
        candidates = set()

        for band in range(self.bands):
            buckets = {}

            start = band * self.rows_per_band
            end = start + self.rows_per_band

            for i, signature in enumerate(signatures):
                key = tuple(signature[start:end])

                if key not in buckets:
                    buckets[key] = []

                buckets[key].append(i)

            for bucket in buckets.values():
                for x in range(len(bucket)):
                    for y in range(x + 1, len(bucket)):
                        i = bucket[x]
                        j = bucket[y]
                        candidates.add((i, j))

        # Only calculate the expensive similarity for candidates
        result = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                result.add((i, j))

        return result
