
#!/usr/bin/env python3
"""Week 4 Task 3 — Same memory, fewer mistakes."""
import hashlib
import math


class NaiveFilter:
    """One hash function, and the bits it was given."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

    def _index(self, item):
        d = hashlib.blake2b(
            str(item).encode(),
            digest_size=8,
            key=str(self.seed).encode()
        ).digest()
        return int.from_bytes(d, "big") % self.n_bits

    def add(self, item):
        self.bits[self._index(item)] = 1

    def __contains__(self, item):
        return bool(self.bits[self._index(item)])

    def memory_bits(self):
        return self.n_bits


class YourFilter:
    """Bloom filter with an optimized number of hash functions."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

        # 8,000 items and 80,000 bits: 10 bits per item.
        self.k = max(1, round(10 * math.log(2)))

    def _indices(self, item):
        data = str(item).encode()
        key = str(self.seed).encode()

        digest = hashlib.blake2b(
            data,
            digest_size=16,
            key=key
        ).digest()

        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:], "big") | 1

        for i in range(self.k):
            yield (h1 + i * h2) % self.n_bits

    def add(self, item):
        for index in self._indices(item):
            self.bits[index] = 1

    def __contains__(self, item):
        return all(
            self.bits[index]
            for index in self._indices(item)
        )

    def memory_bits(self):
        return self.n_bits

