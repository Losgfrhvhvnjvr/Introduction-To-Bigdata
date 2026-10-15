### Task 1 — K-means and initialisation

I chose to keep the previous centroid when a cluster becomes empty. This avoids changing the clustering unexpectedly.

Across 40 seeds, random initialisation produced SSE values from 0.120 to 96.120, while k-means++ had a mean SSE of 0.120. K-means++ generally provides better initial centroids and more reliable clustering results.

SSE tends to decrease when k increases, so minimising SSE alone is not enough to choose the right number of clusters.

### Task 2 — Curse of dimensionality

The distance contrast falls below 1 at dimension 50 and below 0.5 at dimension 200. At dimension 1000, it reaches 0.153, showing that distances become less discriminative as dimensionality increases.

At dimension 20, increasing the number of points from 200 to 2000 increases the observed contrast from 1.787 to 2.448, while the mean distance remains close to 1.82. The observed minimum and maximum depend on the sample size.

These results do not invalidate Week 3 LSH. This experiment measures Euclidean distance between uniformly distributed points, whereas our LSH implementation uses Jaccard similarity on shingle sets. The distance metric and data distribution are different.

### Task 3 — K-means with distance bounds

I store two bounds per point: an upper bound on the distance to its assigned centroid and a lower bound on the distance to competing centroids. This adds two numbers per point, or 40,000 bound values for 20,000 points.

The bounds and the half-distance between centroids allow the algorithm to skip distance calculations when an assignment is guaranteed to remain unchanged. Maintaining the bounds costs centroid-movement calculations and pairwise centroid distances, but this is much cheaper than comparing every point with every centroid.

The final SSE is exactly the same as the baseline (10,737,882.94; difference 0.0000%) because the bounds only prune calculations when the triangle inequality proves that a point cannot change cluster. Uncertain assignments are still checked exactly.

The first iteration performs 240,000 point-to-centroid distance calculations (20,000 × 12), about 17.5% of the total 1,371,762 distance calculations in my implementation. It cannot prune any initial assignments because no valid bounds have been established yet.

The benchmark reduced distance computations by 86.7%, reaching the strong performance level.
