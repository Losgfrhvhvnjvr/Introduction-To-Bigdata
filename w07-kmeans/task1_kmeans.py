
#!/usr/bin/env python3
"""Week 7 · Task 1 — k-means and its initialisation."""
import argparse
import math
import random

# Three obvious blobs of three points each.
BLOBS = [(0.0, 0.0), (0.2, 0.1), (0.1, 0.2),
         (8.0, 8.0), (8.2, 8.1), (8.1, 8.2),
         (0.0, 8.0), (0.2, 8.1), (0.1, 8.2)]


def euclidean(a, b):
    """Distance between two points of any dimension."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def assign(points, centroids):
    """Assign each point to its nearest centroid.
    Ties go to the lower index.
    """
    labels = []
    for point in points:
        distances = [euclidean(point, c) for c in centroids]
        labels.append(min(range(len(centroids)), key=lambda i: distances[i]))
    return labels


def update(points, labels, k):
    """Move centroids to their cluster means.
    Empty clusters keep their previous centroid only if available;
    here, an empty cluster is represented by None.
    """
    if not points:
        return [None] * k

    dimensions = len(points[0])
    centroids = []

    for cluster in range(k):
        members = [p for p, label in zip(points, labels)
                   if label == cluster]

        if not members:
            centroids.append(None)
        else:
            mean = tuple(
                sum(point[d] for point in members) / len(members)
                for d in range(dimensions)
            )
            centroids.append(mean)

    return centroids


def sse_of(points, labels, centroids):
    """Sum of squared distances to assigned centroids."""
    total = 0.0
    for point, label in zip(points, labels):
        distance = euclidean(point, centroids[label])
        total += distance ** 2
    return total


def kmeans(points, k, init="random", seed=246, max_iter=100):
    """Run k-means to convergence. Return (labels, centroids, sse)."""
    if not points:
        raise ValueError("points must not be empty")
    if k < 1 or k > len(points):
        raise ValueError("k must be between 1 and len(points)")
    if init not in ("random", "++"):
        raise ValueError("init must be 'random' or '++'")

    rng = random.Random(seed)
    points = list(points)

    # Choose k distinct starting points.
    if init == "random":
        centroids = [points[i] for i in rng.sample(range(len(points)), k)]
    else:
        centroids = [points[rng.randrange(len(points))]]

        while len(centroids) < k:
            distances_sq = [
                min(euclidean(point, c) ** 2 for c in centroids)
                for point in points
            ]
            total = sum(distances_sq)

            if total == 0:
                # All remaining points coincide with existing centroids.
                candidates = [p for p in points if p not in centroids]
                if not candidates:
                    centroids.append(centroids[0])
                else:
                    centroids.append(rng.choice(candidates))
                continue

            target = rng.random() * total
            cumulative = 0.0
            chosen = points[-1]

            for point, distance_sq in zip(points, distances_sq):
                cumulative += distance_sq
                if cumulative >= target:
                    chosen = point
                    break

            centroids.append(chosen)

    iterations = 0

    for _ in range(max_iter):
        iterations += 1
        labels = assign(points, centroids)
        new_centroids = update(points, labels, k)

        # Keep the old centroid for an empty cluster.
        new_centroids = [
            old if new is None else new
            for old, new in zip(centroids, new_centroids)
        ]

        if new_centroids == centroids:
            centroids = new_centroids
            break

        centroids = new_centroids

    # Reassign using the final centroids.
    labels = assign(points, centroids)
    result_sse = sse_of(points, labels, centroids)
    kmeans.iterations = iterations

    return labels, centroids, result_sse


# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<50} {detail}")
        fails += not ok

    try:
        check("distance in 2d",
              abs(euclidean((0, 0), (3, 4)) - 5) < 1e-9)
        check("distance in 5d",
              abs(euclidean((0,) * 5, (1,) * 5) - math.sqrt(5)) < 1e-9)
    except NotImplementedError:
        print("  euclidean is still a stub")
        return 1

    try:
        labels, cents, sse = kmeans(BLOBS, 3, init="++", seed=1)
    except NotImplementedError:
        print("  kmeans is still a stub")
        return 1

    groups = {}
    for p, l in zip(BLOBS, labels):
        groups.setdefault(l, []).append(p)

    check("three clusters of three",
          sorted(len(g) for g in groups.values()) == [3, 3, 3],
          sorted(len(g) for g in groups.values()))

    check("the three blobs were recovered",
          all(max(q[0] for q in g) - min(q[0] for q in g) < 1 and
              max(q[1] for q in g) - min(q[1] for q in g) < 1
              for g in groups.values()))

    check("sse is small when clusters are right",
          sse < 1.0, f"sse {sse:.4f}")

    randoms = [kmeans(BLOBS, 3, init="random", seed=s)[2]
               for s in range(40)]
    plusplus = [kmeans(BLOBS, 3, init="++", seed=s)[2]
                for s in range(40)]

    check("random init sometimes lands badly",
          max(randoms) > min(randoms) * 5,
          f"sse from {min(randoms):.3f} to {max(randoms):.3f}")

    check("k-means++ is more reliable than random",
          sum(plusplus) / len(plusplus) <= sum(randoms) / len(randoms),
          f"mean sse: ++ {sum(plusplus) / len(plusplus):.3f} vs "
          f"random {sum(randoms) / len(randoms):.3f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())

