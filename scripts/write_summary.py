#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path("output")

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_md_table(rows, headers):
    widths = {}
    for h in headers:
        widths[h] = max(len(h), *(len(str(row[h])) for row in rows)) if rows else len(h)

    def fmt_row(row):
        cells = [str(row[h]).ljust(widths[h]) for h in headers]
        return "| " + " | ".join(cells) + " |"

    sep = "| " + " | ".join("-" * widths[h] for h in headers) + " |"

    out = [fmt_row({h: h for h in headers}), sep]
    for row in rows:
        out.append(fmt_row(row))
    return "\n".join(out)

def ns_iter_to_us(value_str):
    return float(value_str) / 1000.0

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
        {
            "Benchmark": row["benchmark"],
            "Median": f'{ns_iter_to_us(row["median_estimate"]):.4f} µs/iter'
        }
        for row in spqr
    ]
    chain_rows = [
        {
            "Benchmark": row["benchmark"],
            "Median": f'{ns_iter_to_us(row["median_estimate"]):.4f} µs/iter'
        }
        for row in chain
    ]

    md = []
    md.append("# Benchmark summary\n")
    md.append("## libsignal version comparison\n")
    md.append(write_md_table(comparison_rows, [
        "Old version",
        "New version",
        "Old median",
        "New median",
        "Absolute difference",
        "% difference",
    ]))
    md.append("\n## Standalone SPQR (`benches/spqr.rs`)\n")
    md.append(write_md_table(spqr_rows, ["Benchmark", "Median"]))
    md.append("\n## Standalone SPQR chain (`benches/chain.rs`)\n")
    md.append(write_md_table(chain_rows, ["Benchmark", "Median"]))
    (ROOT / "summary.md").write_text("\n".join(md), encoding="utf-8")

if __name__ == "__main__":
    main()
