import re
import sys
import csv
from pathlib import Path

TARGETS = [
    "tests::init_a",
    "tests::init_b",
    "tests::long_chain_send",
    "tests::send_recv",
    "tests::add_epoch",
    "tests::recv_key",
    "tests::recv_skip_key",
    "tests::recv_with_truncate",
    "tests::send_key",
]

# Example:
# test tests::send_recv       ... bench:      23,230.39 ns/iter (+/- 1,280.82)
BENCH_RE = re.compile(
    r"test\s+(tests::[A-Za-z0-9_]+)\s+\.\.\.\s+bench:\s+([0-9,]+\.[0-9]+)\s+([a-zµ/]+)\s+\(\+/-\s+([0-9,]+\.[0-9]+)\)"
)

def parse_file(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    results = []

    for line in lines:
        m = BENCH_RE.search(line)
        if not m:
            continue

        bench, estimate, unit, plusminus = m.groups()
        if bench not in TARGETS:
            continue

        results.append({
            "file": path.name,
            "benchmark": bench,
            "estimate": estimate.replace(",", ""),
            "unit": unit,
            "plusminus": plusminus.replace(",", ""),
        })

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_spqr_benches.py <file1> [file2 ...]")
        sys.exit(1)

    all_results = []
    for arg in sys.argv[1:]:
        all_results.extend(parse_file(Path(arg)))

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["file", "benchmark", "estimate", "unit", "plusminus"]
    )
    writer.writeheader()
    writer.writerows(all_results)

if __name__ == "__main__":
    main()
