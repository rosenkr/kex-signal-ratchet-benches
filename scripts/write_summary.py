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

    def escape_cell(value):
        return str(value).replace("|", "\\|")

    def fmt_row(row):
        cells = [escape_cell(row[h]).ljust(widths[h]) for h in headers]
        return "| " + " | ".join(cells) + " |"

    sep = "| " + " | ".join("-" * widths[h] for h in headers) + " |"

    out = [fmt_row({h: h for h in headers}), sep]
    for row in rows:
        out.append(fmt_row(row))
    return "\n".join(out)


def criterion_range(row):
    return (
        f"[{row['low']} {row['low_unit']} "
        f"{row['estimate']} {row['estimate_unit']} "
        f"{row['high']} {row['high_unit']}]"
    )


def spqr_value(row):
    return f"{row['estimate']} {row['unit']} (+/- {row['plusminus']})"


def main():
    v073 = read_csv(ROOT / "v073_3" / "session_values.csv")
    v092 = read_csv(ROOT / "v092_1" / "session_values.csv")
    spqr = read_csv(ROOT / "spqr" / "spqr_values.csv")
    chain = read_csv(ROOT / "spqr" / "chain_values.csv")

    v073_map = {row["benchmark"]: row for row in v073}
    v092_map = {row["benchmark"]: row for row in v092}

    pairs = [
        ("session encrypt", "encrypting on an existing chain"),
        ("session decrypt", "decrypting on an existing chain"),
        ("session encrypt+decrypt 1 way", "session encrypt+decrypt 1 way"),
        ("session encrypt+decrypt ping pong", "session encrypt+decrypt ping pong"),
    ]

    comparison_rows = []
    for v073_name, v092_name in pairs:
        comparison_rows.append({
            "v0.73.3 benchmark": v073_name,
            "v0.92.1 benchmark": v092_name,
            "v0.73.3 sampling": v073_map[v073_name]["samples"] or "-",
            "v0.73.3 measured total": v073_map[v073_name]["measured_total"] or "-",
            "v0.73.3 R²": v073_map[v073_name]["r_squared"] or "-",
            "v0.73.3 time": criterion_range(v073_map[v073_name]),
            "v0.73.3 sends/recvs": f"{v073_map[v073_name]['sends'] or '-'} / {v073_map[v073_name]['recvs'] or '-'}",
            "v0.73.3 DR sym": v073_map[v073_name]["dr_symmetric"] or "-",
            "v0.73.3 DR DH": v073_map[v073_name]["dr_dh"] or "-",
            "v0.92.1 sampling": v092_map[v092_name]["samples"] or "-",
            "v0.92.1 measured total": v092_map[v092_name]["measured_total"] or "-",
            "v0.92.1 R²": v092_map[v092_name]["r_squared"] or "-",
            "v0.92.1 time": criterion_range(v092_map[v092_name]),
            "v0.92.1 sends/recvs": f"{v092_map[v092_name]['sends'] or '-'} / {v092_map[v092_name]['recvs'] or '-'}",
            "v0.92.1 DR sym": v092_map[v092_name]["dr_symmetric"] or "-",
            "v0.92.1 DR DH": v092_map[v092_name]["dr_dh"] or "-",
            "v0.92.1 SPQR sym": v092_map[v092_name]["spqr_symmetric"] or "-",
            "v0.92.1 Braid": v092_map[v092_name]["braid_add_epoch"] or "-",
        })

    spqr_rows = [
        {
            "Benchmark": row["benchmark"],
            "Reported value": spqr_value(row),
        }
        for row in spqr
    ]

    chain_rows = [
        {
            "Benchmark": row["benchmark"],
            "Reported value": spqr_value(row),
        }
        for row in chain
    ]

    md = []
    md.append("# Benchmark summary\n")
    md.append("Raw logs and parsed single-run values are stored under `output/`.\n")

    md.append("## Comparison of libsignal v0.73.3 and v0.92.1 \n")
    md.append(write_md_table(comparison_rows, [
        "v0.73.3 benchmark",
        "v0.92.1 benchmark",
        "v0.73.3 sampling",
        "v0.73.3 measured total",
        "v0.73.3 R²",
        "v0.73.3 time",
        "v0.73.3 sends/recvs",
        "v0.73.3 DR sym",
        "v0.73.3 DR DH",
        "v0.92.1 sampling",
        "v0.92.1 measured total",
        "v0.92.1 R²",
        "v0.92.1 time",
        "v0.92.1 sends/recvs",
        "v0.92.1 DR sym",
        "v0.92.1 DR DH",
        "v0.92.1 SPQR sym",
        "v0.92.1 Braid",
    ]))

    md.append("\n## Standalone SPQR (`benches/spqr.rs`)\n")
    md.append(write_md_table(spqr_rows, ["Benchmark", "Reported value"]))

    md.append("\n## Standalone SPQR (`benches/chain.rs`)\n")
    md.append(write_md_table(chain_rows, ["Benchmark", "Reported value"]))

    summary_path = ROOT / "summary.md"
    summary_path.unlink(missing_ok=True)
    summary_path.write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
