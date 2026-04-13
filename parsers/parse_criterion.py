import re
import sys
import csv
from pathlib import Path

TARGETS = [
    "encrypting on an existing chain",
    "decrypting on an existing chain",
    "session encrypt+decrypt 1 way",
    "session encrypt+decrypt ping pong",
    "session encrypt",
    "session decrypt",
]

TIME_RE = re.compile(
    r"time:\s*\[\s*([0-9.]+)\s*([^\s]+)\s+([0-9.]+)\s*([^\s]+)\s+([0-9.]+)\s*([^\s]+)\s*\]"
)

def parse_file(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    results = []
    seen = set()

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        for target in TARGETS:
            if line == target:
                for j in range(i + 1, min(i + 8, len(lines))):
                    m = TIME_RE.search(lines[j])
                    if m:
                        low_val, low_unit, mid_val, mid_unit, high_val, high_unit = m.groups()
                        key = (path.name, target)
                        if key not in seen:
                            results.append({
                                "file": path.name,
                                "benchmark": target,
                                "low": low_val,
                                "estimate": mid_val,
                                "high": high_val,
                                "unit": mid_unit,
                            })
                            seen.add(key)
                        break

            elif line.startswith(target) and "time:" in line:
                m = TIME_RE.search(line)
                if m:
                    low_val, low_unit, mid_val, mid_unit, high_val, high_unit = m.groups()
                    key = (path.name, target)
                    if key not in seen:
                        results.append({
                            "file": path.name,
                            "benchmark": target,
                            "low": low_val,
                            "estimate": mid_val,
                            "high": high_val,
                            "unit": mid_unit,
                        })
                        seen.add(key)

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_criterion.py <file1> [file2 ...]")
        sys.exit(1)

    all_results = []
    for arg in sys.argv[1:]:
        all_results.extend(parse_file(Path(arg)))

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["file", "benchmark", "low", "estimate", "high", "unit"]
    )
    writer.writeheader()
    writer.writerows(all_results)

if __name__ == "__main__":
    main()
