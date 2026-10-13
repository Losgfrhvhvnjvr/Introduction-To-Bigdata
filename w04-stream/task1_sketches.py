
#!/usr/bin/env python3
"""Week 4 - Task 1: Mining Data Streams."""

import argparse
import hashlib
import math
import random
import statistics


class BloomFilter:
    """Bloom filter: no false negatives, possible false positives."""

    def __init__(self, m, k, seed=246):
        self.m = m
        self.k = k
        self.seed = seed
        self.bits = bytearray((m + 7) // 8)

    def _hashes(self, item):
        data = repr(item).encode("utf-8")
        seed_bytes = self.seed.to_bytes(8, "little", signed=True)
        digest = hashlib.blake2b(
            data + seed_bytes, digest_size=16
        ).digest()

        h1 = int.from_bytes(digest[:8], "little")
        h2 = int.from_bytes(digest[8:], "little") | 1

        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item):
        for position in self._hashes(item):
            byte_index = position >> 3
            bit_mask = 1 << (position & 7)
            self.bits[byte_index] |= bit_mask

    def __contains__(self, item):
        return all(
            self.bits[position >> 3] & (1 << (position & 7))
            for position in self._hashes(item)
        )
    def expected_fp_rate(self, n_inserted):
        """Theoretical false-positive rate from section 4.4.2."""
        return (1 - math.exp(-self.k * n_inserted / self.m)) ** self.k



def flajolet_martin(stream, n_hashes=16, seed=246):
    """Estimate the number of distinct items in a stream."""
    maxima = [0] * n_hashes
    seed_bytes = seed.to_bytes(8, "little", signed=True)

    for item in stream:
        data = repr(item).encode("utf-8") + seed_bytes

        # Generate up to 8 independent 64-bit hash values per digest.
        for round_index in range((n_hashes + 7) // 8):
            digest = hashlib.blake2b(
                data + bytes([round_index]),
                digest_size=64
            ).digest()

            start = round_index * 8
            count = min(8, n_hashes - start)

            for j in range(count):
                x = int.from_bytes(
                    digest[j * 8:(j + 1) * 8], "little"
                )

                zeros = 64 if x == 0 else (x & -x).bit_length() - 1
                if zeros > maxima[start + j]:
                    maxima[start + j] = zeros

    estimates = [
        0.77351 * (2 ** value) for value in maxima
    ]

    group_size = 8
    group_estimates = [
        statistics.median(estimates[i:i + group_size])
        for i in range(0, n_hashes, group_size)
    ]

    return float(statistics.median(group_estimates))



def reservoir_sample(stream, k, seed=246):
    """Uniformly sample up to k items from a stream of unknown length."""
    if k <= 0:
        return []

    rng = random.Random(seed)
    reservoir = []

    for index, item in enumerate(stream):
        if index < k:
            reservoir.append(item)
        else:
            j = rng.randrange(index + 1)
            if j < k:
                reservoir[j] = item

    return reservoir


def verify():
    fails = 0
    rng = random.Random(246)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<46} {detail}")
        if not ok:
            fails += 1

    # Bloom filter: no false negatives
    bf = BloomFilter(m=8192, k=5)
    inserted = [f"item-{i}" for i in range(800)]

    for item in inserted:
        bf.add(item)

    check("no false negatives", all(item in bf for item in inserted))

    # Compare measured and predicted false-positive rates
    absent = [f"other-{i}" for i in range(20_000)]
    fp = sum(item in bf for item in absent) / len(absent)
    predicted = bf.expected_fp_rate(len(inserted))
    close = abs(fp - predicted) < max(0.02, predicted * 0.5)

    check(
        "measured false-positive rate matches theory",
        close,
        f"measured {fp:.3%}, predicted {predicted:.3%}"
    )

    # Flajolet-Martin: estimate distinct count
    distinct = 20_000
    stream = [
        f"k{rng.randrange(distinct)}"
        for _ in range(120_000)
    ]

    estimate = flajolet_martin(stream)
    true_distinct = len(set(stream))
    ratio = estimate / true_distinct

    check(
        "distinct estimate within a factor of 2",
        0.5 <= ratio <= 2.0,
        f"estimated {estimate:,.0f}, true {true_distinct:,} "
        f"({ratio:.2f}x)"
    )

    # Reservoir sampling: uniformity across 4,000 trials
    counts = [0] * 20
    trials = 4000

    for t in range(trials):
        sample = reservoir_sample(range(20), 5, seed=t)
        for item in sample:
            counts[item] += 1

    expected = trials * 5 / 20
    spread = (max(counts) - min(counts)) / expected

    check(
        "reservoir is uniform across items",
        spread < 0.15,
        f"spread {spread:.1%} around {expected:.0f}"
    )

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    raise SystemExit(verify() if args.verify else parser.print_help())
