# Week 5 — Task 2: PageRank convergence

## A3 — Effect of beta on convergence

The number of iterations generally increases as beta approaches 1. On the 1,200-node graph, convergence required 14 iterations for beta = 0.5, 17 for 0.7, 20 for 0.85, 23 for 0.95, and 24 for 0.99. A larger beta means that the algorithm follows links more often and teleports less frequently. This weakens the regularizing effect of teleportation and can slow convergence.

## A4 — Effect of graph size

For beta = 0.85, the 1,200-node graph required 20 iterations and 0.056 seconds, while the 20,000-node graph required 21 iterations and 0.630 seconds. For beta = 0.95, the corresponding results were 23 iterations and 0.062 seconds versus 24 iterations and 0.872 seconds.

The iteration count increased by only one in both comparisons, while execution time increased substantially. Each iteration processes more nodes and edges in the larger graph, so the computation takes longer even though the number of iterations remains similar.

## A5 — Effect of tolerance

For beta = 0.85 on the 1,200-node graph, tolerance 1e-10 required 20 iterations, while tolerance 1e-6 required 12 iterations. The stricter tolerance required 8 additional iterations. A stricter tolerance requires a smaller difference between consecutive PageRank vectors before stopping, so more iterations are generally needed. These two measurements alone do not establish a fixed cost per additional decimal digit.

## A6 — Stability of the top-10 ranking

For beta = 0.5, p00000 ranked above p00004. Starting at beta = 0.7, p00004 ranked above p00000. Thus, the first observed top-10 ordering change occurred at beta = 0.7. The top three pages remained p00009, p00001, and p00006 for all five tested beta values.

This suggests that the highest-ranked pages were stable in this experiment, but some lower positions depended on beta. Rankings should therefore be interpreted with their model assumptions in mind.

## A7 — Machine and environment

- Operating system: Windows 11
- CPU: 12th Gen Intel(R) Core(TM) i7-1255U
- Installed RAM: approximately 15.7 GiB
- Python: 3.13.15
- Other programs running during the measurements: Google Chrome, Spyder, Outlook, and VS Code

