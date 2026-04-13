#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path("output")

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_table(rows, headers):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(out)

def main():
    v073 = read_csv(ROOT / "v073_3" / "session_medians.csv")
    v092 = read_csv(ROOT / "v092_1" / "session_medians.csv")
    spqr = read_csv(ROOT / "spqr" / "spqr_medians.csv")
    chain = read_csv(ROOT / "spqr" / "chain_medians.csv")

    old_map = {row["benchmark"]: row for row in v073}
    new_map = {row["benchmark"]: row for row in v092}

    pairs = [
        ("session encrypt", "encrypting on an existing chain"),
        ("session decrypt", "decrypting on an existing chain"),
        ("session encrypt+decrypt 1 way", "session encrypt+decrypt 1 way"),
        ("session encrypt+decrypt ping pong", "session encrypt+decrypt ping pong"),
    ]

    comparison_rows = []
    for old_name, new_name in pairs:
        old_val = float(old_map[old_name]["median_estimate"])
        new_val = float(new_map[new_name]["median_estimate"])
        diff = new_val - old_val
        pct = (diff / old_val) * 100.0
        comparison_rows.append({
            "Old version": old_name,
            "New version": new_name,
            "Old median": f"{old_val:.4f} µs",
            "New median": f"{new_val:.4f} µs",
            "Absolute difference": f"{diff:+.4f} µs",
            "% difference": f"{pct:+.2f}%",
        })

    spqr_rows = [
        {"Benchmark": row["benchmark"], "Median": f'{row["median_estimate"]} {row["unit"]}'}
        for row in spqr
    ]
    chain_rows = [
        {"Benchmark": row["benchmark"], "Median": f'{row["median_estimate"]} {row["unit"]}'}
        for row in chain
    ]

    text = []
    text.append("# Benchmark summary\n")
    text.append("## libsignal version comparison\n")
    text.append(write_table(comparison_rows, [
        "Old version",
        "New version",
        "Old median",
        "New median",
        "Absolute difference",
        "% difference",
    ]))
    text.append("\n## Standalone SPQR (`benches/spqr.rs`)\n")
    text.append(write_table(spqr_rows, ["Benchmark", "Median"]))
    text.append("\n## Standalone SPQR chain (`benches/chain.rs`)\n")
    text.append(write_table(chain_rows, ["Benchmark", "Median"]))
    (ROOT / "summary.md").write_text("\n".join(text), encoding="utf-8")

if __name__ == "__main__":
    main()
