# Week 5 — Observations

## Task 1 — PageRank, dead ends, and spider traps

Without teleportation and without handling dead ends, PageRank can lose rank mass. A page with no outgoing links does not pass its rank to any other page, so the total rank can decrease after each iteration.

The corrected PageRank algorithm redistributes the rank of dead-end pages uniformly across all nodes. This preserves the total rank.

Teleportation also helps solve the spider-trap problem. At each iteration, every page receives a small amount of rank through the teleportation term. This allows the random surfer to leave a closed group of pages instead of remaining trapped there.

The parameter beta is the probability of following a link. The probability of teleporting is 1 - beta.

## Task 3 — Why sparse PageRank avoids a dense matrix

The dense baseline stores an n-by-n matrix, which requires O(n^2) memory. The sparse implementation uses the adjacency list and stores rank values for the nodes, so it avoids storing all possible node-to-node connections.

The teleportation term is (1 - beta) / n for every node. It is the same constant for all nodes, so the algorithm can initialise each new rank with this value in O(n) time instead of building a dense teleportation matrix.

Dead-end rank can also be handled efficiently: sum the rank of all dead-end nodes, divide it uniformly among all nodes, and add that share to each new rank. Link contributions are then distributed by iterating over the actual outgoing edges.

This sparse approach uses much less memory on a sparse graph while producing PageRank values that match the dense baseline within the required tolerance of 1e-9.
