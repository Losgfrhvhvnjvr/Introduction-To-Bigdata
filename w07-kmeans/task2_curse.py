#!/usr/bin/env python3
"""Week 7 · Task 2 — Watch distance stop meaning anything.

Textbook §7.1.3, the curse of dimensionality.

In two dimensions "nearest" is obvious. In two hundred, every point is roughly
the same distance from every other point, and a method built on "nearest" has
nothing left to stand on.

That is usually stated as a fact to accept. Here you measure it, on your own
machine, and find the dimension where it starts to bite for **your** data size.

    python3 task2_curse.py --dims 2,5,10,20,50,100,200
    python3 task2_curse.py --dims 500,1000 --points 2000

The contrast ratio is the number to watch.
"""
import argparse, json, math, os, platform, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def machine():
    return {"platform": platform.platform(),
            "processor": platform.processor() or platform.machine(),
            "python": platform.python_version()}


def euclid(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def sample_distances(n, dim, pairs, seed=246):
    rng = random.Random(seed + dim)
    pts = [tuple(rng.random() for _ in range(dim)) for _ in range(n)]
    ds = []
    for _ in range(pairs):
        i, j = rng.randrange(n), rng.randrange(n)
        if i != j:
            ds.append(euclid(pts[i], pts[j]))
    return ds


def write_report(runs, machine_info):
    """Generate the Markdown report from all recorded measurements."""
    path = os.path.join(OUT, "curse.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Week 7 — Task 2: Curse of dimensionality\n\n")
        f.write("## Measurements\n\n")
        f.write("| Dimension | Points | Pairs | Mean | Min | Max | "
                "Contrast | Relative SD | Seconds |\n")
        f.write("|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")

        for r in sorted(runs, key=lambda x: (x["points"], x["dim"])):
            f.write(
                f'| {r["dim"]} | {r["points"]} | {r["pairs"]} '
                f'| {r["mean"]:.4f} | {r["min"]:.4f} '
                f'| {r["max"]:.4f} | {r["contrast"]:.4f} '
                f'| {r["relative_stdev"]:.4f} | {r["seconds"]:.2f} |\n'
            )

        # Use the default 1,000-point measurements to discuss dimensions.
        baseline = sorted(
            (r for r in runs if r["points"] == 1000),
            key=lambda r: r["dim"]
        )

        f.write("\n## A3 — Contrast thresholds\n\n")
        if baseline:
            for threshold in (1.0, 0.5):
                found = next(
                    (r for r in baseline
                     if r["contrast"] < threshold),
                    None
                )
                if found:
                    f.write(
                        f'- Contrast first falls below {threshold} at '
                        f'dimension {found["dim"]} '
                        f'(contrast {found["contrast"]:.4f}).\n'
                    )
                else:
                    f.write(
                        f'- Contrast does not fall below {threshold} '
                        'in the measured dimensions.\n'
                    )

            f.write("\n## A4 — Mean distance\n\n")
            f.write(
                "For uniformly distributed points in a unit cube, "
                "the mean Euclidean distance is expected to grow "
                "approximately as the square root of dimension, "
                "rather than linearly. The mean/sqrt(d) ratios below "
                "help assess this trend:\n\n"
            )
            f.write("| Dimension | Mean | Mean / sqrt(d) |\n")
            f.write("|---:|---:|---:|\n")
            for r in baseline:
                f.write(
                    f'| {r["dim"]} | {r["mean"]:.4f} '
                    f'| {r["mean"] / math.sqrt(r["dim"]):.4f} |\n'
                )
        else:
            f.write(
                "Run the default experiment with --points 1000 "
                "to analyse the dimension thresholds.\n"
            )

        f.write("\n## A5 — Relative standard deviation\n\n")
        if baseline:
            for r in baseline:
                f.write(
                    f'- Dimension {r["dim"]}: relative SD = '
                    f'{r["relative_stdev"]:.4f}.\n'
                )
            f.write(
                "\nContrast uses the two extreme sampled distances and "
                "is sensitive to sample size. Relative SD measures the "
                "overall dispersion relative to the mean, so it often "
                "gives a more stable picture of distance concentration.\n"
            )

        f.write("\n## A6 — Effect of point count\n\n")
        comparisons = [r for r in runs if r["dim"] == 20]
        counts = {r["points"] for r in comparisons}
        if len(counts) >= 2:
            f.write(
                "At dimension 20, the observed contrast changes with "
                "point count:\n\n"
            )
            for r in sorted(comparisons, key=lambda r: r["points"]):
                f.write(
                    f'- {r["points"]} points: contrast = '
                    f'{r["contrast"]:.4f}, min = {r["min"]:.4f}, '
                    f'max = {r["max"]:.4f}.\n'
                )
            f.write(
                "\nThe minimum and maximum are sample extremes, so "
                "their gap can change as the number of sampled points "
                "increases. The random sampling also introduces "
                "variation between runs.\n"
            )
        else:
            f.write(
                "Compare at least two point counts at dimension 20. "
                "For example, run with --dims 20 --points 200, then "
                "--dims 20 --points 1000, and "
                "--dims 20 --points 2000.\n"
            )

        f.write("\n## A7 — Machine and runtime\n\n")
        f.write(f'- Platform: {machine_info["platform"]}\n')
        f.write(f'- Processor: {machine_info["processor"]}\n')
        f.write(f'- Python: {machine_info["python"]}\n')
        if runs:
            longest = max(runs, key=lambda r: r["seconds"])
            f.write(
                f'- Longest recorded measurement: dimension '
                f'{longest["dim"]}, {longest["points"]} points, '
                f'{longest["seconds"]:.2f} seconds.\n'
            )

        f.write("\n## A8 — Connection to Week 3 LSH\n\n")
        f.write(
            "These results do not automatically invalidate LSH from "
            "Week 3. This experiment measures Euclidean distances "
            "between uniformly distributed points in a unit cube, "
            "whereas the Week 3 method uses Jaccard similarity on "
            "shingle sets. The distance metric and data distribution "
            "are different. LSH performance must be evaluated for "
            "the relevant similarity measure and dataset.\n"
        )

    print("  -> out/curse.md")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dims", default="2,5,10,20,50,100,200")
    p.add_argument("--points", type=int, default=1000)
    p.add_argument("--pairs", type=int, default=20000)
    a = p.parse_args()
    os.makedirs(OUT, exist_ok=True)

    rows = []
    for dim in [int(x) for x in a.dims.split(",")]:
        t0 = time.perf_counter()
        ds = sample_distances(a.points, dim, a.pairs)
        elapsed = time.perf_counter() - t0
        lo, hi = min(ds), max(ds)
        mean = sum(ds) / len(ds)
        var = sum((d - mean) ** 2 for d in ds) / len(ds)
        row = {"dim": dim, "points": a.points, "pairs": len(ds),
               "min": lo, "max": hi, "mean": mean,
               "stdev": math.sqrt(var),
               "contrast": (hi - lo) / lo if lo else None,
               "relative_stdev": math.sqrt(var) / mean if mean else None,
               "seconds": elapsed}
        rows.append(row)
        print(f"  dim {dim:>5}   mean {mean:>7.3f}   min {lo:>7.3f}   "
              f"max {hi:>7.3f}   contrast {row['contrast']:>7.3f}   "
              f"rel.sd {row['relative_stdev']:>6.3f}")

        
    path = os.path.join(OUT, "curse.json")

    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            prior = json.load(f)
    else:
        prior = {"runs": []}

    prior["machine"] = machine()
    prior["runs"].extend(rows)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(prior, f, indent=2)

    write_report(prior["runs"], prior["machine"])
    print(f"\n  -> out/curse.json ({len(prior['runs'])} measurement(s))")




if __name__ == "__main__":
    main()
