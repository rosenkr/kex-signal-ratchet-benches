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


def ns_to_us(value_str):
    return float(value_str) / 1000.0


def ns2_to_us2(value_str):
    return float(value_str) / 1_000_000.0


def fmt_us(value):
    return f"{value:.2f} µs"


def fmt_us_diff(value):
    return f"{value:+.2f} µs"


def fmt_us_per_iter(value):
    return f"{value:.2f} µs/iter"


def fmt_us_sq(value):
    return f"{value:.2f} µs²"


def fmt_us2_per_iter2(value):
    return f"{value:.2f} (µs/iter)^2"


def fmt_pct(value):
    return f"{value:+.2f}%"


def main():
    v073 = read_csv(ROOT / "v073_3" / "session_medians.csv")
    v092 = read_csv(ROOT / "v092_1" / "session_medians.csv")
    spqr = read_csv(ROOT / "spqr" / "spqr_medians.csv")

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
        v073_median = float(v073_map[v073_name]["median_estimate"])
        v092_median = float(v092_map[v092_name]["median_estimate"])
        median_diff = v092_median - v073_median
        median_pct = (median_diff / v073_median) * 100.0

        v073_mean = float(v073_map[v073_name]["mean_estimate"])
        v092_mean = float(v092_map[v092_name]["mean_estimate"])
        mean_diff = v092_mean - v073_mean

        v073_variance = float(v073_map[v073_name]["variance_estimate"])
        v092_variance = float(v092_map[v092_name]["variance_estimate"])
        variance_diff = v092_variance - v073_variance

        comparison_rows.append({
            "v0.73.3 benchmark": v073_name,
            "v0.92.1 benchmark": v092_name,
            "v0.73.3 median": fmt_us(v073_median),
            "v0.92.1 median": fmt_us(v092_median),
            "Median abs diff": fmt_us_diff(median_diff),
            "% difference": fmt_pct(median_pct),
            "v0.73.3 mean": fmt_us(v073_mean),
            "v0.92.1 mean": fmt_us(v092_mean),
            "Mean abs diff": fmt_us_diff(mean_diff),
            "v0.73.3 variance": fmt_us_sq(v073_variance),
            "v0.92.1 variance": fmt_us_sq(v092_variance),
            "Variance abs diff": fmt_us_diff(variance_diff).replace(" µs", " µs²"),
        })

    spqr_rows = [
        {
            "Benchmark": row["benchmark"],
            "Median": fmt_us_per_iter(ns_to_us(row["median_estimate"])),
            "Mean": fmt_us_per_iter(ns_to_us(row["mean_estimate"])),
            "Variance": fmt_us2_per_iter2(ns2_to_us2(row["variance_estimate"])),
        }
        for row in spqr
    ]

    md = []
    md.append("# Benchmark summary\n")

    md.append("## Comparison of libsignal v0.73.3 and v0.92.1 \n")
    md.append(write_md_table(comparison_rows, [
        "v0.73.3",
        "v0.92.1",
        "v0.73.3 median",
        "v0.92.1 median",
        "Median abs diff",
        "% difference",
        "v0.73.3 mean",
        "v0.92.1 mean",
        "Mean abs diff",
        "v0.73.3 variance",
        "v0.92.1 variance",
        "Variance abs diff",
    ]))

    md.append("\n## Standalone SPQR (`benches/spqr.rs`)\n")

    md.append(write_md_table(spqr_rows, ["Benchmark", "Median", "Mean", "Variance"]))

    (ROOT / "summary.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()