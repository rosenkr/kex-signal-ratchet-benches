import csv
import sys
from statistics import median
from collections import defaultdict

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 median_criterion.py <input.csv>")
        sys.exit(1)

    groups = defaultdict(list)
    unit_for = {}

    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bench = row["benchmark"]
            groups[bench].append(float(row["estimate"]))
            unit_for[bench] = row["unit"]

    writer = csv.writer(sys.stdout)
    writer.writerow(["benchmark", "runs", "median_estimate", "unit", "all_estimates"])

    for bench in sorted(groups):
        vals = groups[bench]
        writer.writerow([
            bench,
            len(vals),
            f"{median(vals):.4f}",
            unit_for[bench],
            " | ".join(f"{v:.4f}" for v in vals),
        ])

if __name__ == "__main__":
    main()
