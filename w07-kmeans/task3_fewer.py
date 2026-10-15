#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out



class YourKMeans:
    """K-means with Hamerly-style bounds to prune distance calculations."""

    def __init__(self, k, max_iter=50):
        self.k = k
        self.max_iter = max_iter
        self.iterations = 0

    def run(self, points, initial_centroids, distance):
        points = list(points)
        centroids = list(initial_centroids)
        n = len(points)
        k = self.k

        if n == 0 or k == 0:
            return [], centroids

        labels = [None] * n
        upper = [0.0] * n
        lower = [0.0] * n
        half_sep = [0.0] * k

        for iteration in range(1, self.max_iter + 1):
            changed = False

            if iteration == 1:
                # First iteration: assign every point exactly.
                # Store the distance to its assigned centroid and
                # the nearest distance to any competing centroid.
                for i, p in enumerate(points):
                    ds = [distance(p, c) for c in centroids]

                    best_idx = 0
                    for j in range(1, k):
                        if ds[j] < ds[best_idx] - 1e-12:
                            best_idx = j

                    labels[i] = best_idx
                    upper[i] = ds[best_idx]
                    lower[i] = min(
                        (ds[j] for j in range(k) if j != best_idx),
                        default=float("inf")
                    )
                    changed = True

            else:
                # Bounds have already been adjusted for centroid motion.
                for i, p in enumerate(points):
                    own = labels[i]

                    # If either bound proves the assignment safe,
                    # skip all point-to-centroid distances.
                    if upper[i] + 1e-12 < max(
                        lower[i], half_sep[own]
                    ):
                        continue

                    # Recompute the exact distance to the current centroid.
                    own_dist = distance(p, centroids[own])
                    upper[i] = own_dist

                    # Only uncertain points need comparisons with others.
                    ds = {own: own_dist}
                    for j, c in enumerate(centroids):
                        if j != own:
                            ds[j] = distance(p, c)

                    best_idx = 0
                    for j in range(1, k):
                        if ds[j] < ds[best_idx] - 1e-12:
                            best_idx = j

                    if labels[i] != best_idx:
                        labels[i] = best_idx
                        changed = True

                    upper[i] = ds[best_idx]
                    lower[i] = min(
                        (ds[j] for j in range(k) if j != best_idx),
                        default=float("inf")
                    )

            self.iterations = iteration
            new_centroids = _means(
                points, labels, k, centroids
            )

            # Measure centroid movements and update point bounds.
            shifts = [
                distance(old, new)
                for old, new in zip(centroids, new_centroids)
            ]
            max_shift = max(shifts, default=0.0)

            for i in range(n):
                upper[i] += shifts[labels[i]]
                lower[i] = max(0.0, lower[i] - max_shift)

            centroids = new_centroids

            # Half the distance to the nearest other centroid is
            # a second safe bound for every point in that cluster.
            half_sep = [float("inf")] * k
            for j in range(k):
                for q in range(j + 1, k):
                    d = distance(centroids[j], centroids[q])
                    half_sep[j] = min(half_sep[j], d / 2.0)
                    half_sep[q] = min(half_sep[q], d / 2.0)

            if not changed:
                break

        return labels, centroids

