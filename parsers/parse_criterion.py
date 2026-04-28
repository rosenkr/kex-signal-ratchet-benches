import argparse
import csv
import json
import re
import sys
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
COLLECTING_RE = re.compile(
    r"Collecting\s+(\d+)\s+samples.*\(([^)]+iterations)\)"
)
R_SQUARED_RE = re.compile(
    r"<td>R&#xb2;</td>\s*"
    r"<td class=\"ci-bound\">([^<]+)</td>\s*"
    r"<td>([^<]+)</td>\s*"
    r"<td class=\"ci-bound\">([^<]+)</td>"
)
RATCHET_RE = re.compile(
    r'\[ratchet-counts\]\s+version=(\S+)\s+bench="([^"]+)"\s+'
    r"iterations=(\d+)\s+sends=(\d+)\s+recvs=(\d+)\s+"
    r"dr_symmetric=(\d+)\s+dr_dh=(\d+)\s+"
    r"spqr_symmetric=(\d+)\s+braid_add_epoch=(\d+)"
)


def fmt_2(value):
    return f"{float(value):.2f}"


def normalize_unit(unit):
    return "µs" if unit == "us" else unit


def format_int(value):
    return f"{int(round(value)):,}"


def find_samples_from_log(lines, start_idx, end_idx):
    for idx in range(start_idx, end_idx):
        collecting_match = COLLECTING_RE.search(lines[idx])
        if collecting_match:
            sample_count, iterations = collecting_match.groups()
            return f"{sample_count} samples, {iterations}"
    return ""


def load_criterion_metrics(criterion_root: Path | None, benchmark: str):
    if criterion_root is None:
        return {}

    bench_root = criterion_root / benchmark
    sample_path = bench_root / "new" / "sample.json"
    report_path = bench_root / "report" / "index.html"

    metrics = {}

    if sample_path.exists():
        sample = json.loads(sample_path.read_text(encoding="utf-8"))
        iters = sample.get("iters", [])
        times = sample.get("times", [])
        if iters:
            metrics["samples"] = (
                f"{len(iters)} samples, {format_int(sum(iters))} iterations"
            )
        if times:
            metrics["measured_total"] = f"{fmt_2(sum(times) / 1_000_000_000.0)} s"

    if report_path.exists():
        report = report_path.read_text(encoding="utf-8", errors="replace")
        r_squared_match = R_SQUARED_RE.search(report)
        if r_squared_match:
            _, point_estimate, _ = r_squared_match.groups()
            metrics["r_squared"] = fmt_2(point_estimate)

    return metrics


def load_ratchet_metrics(lines):
    metrics = {}
    for raw_line in lines:
        match = RATCHET_RE.search(raw_line)
        if not match:
            continue
        (
            _version,
            benchmark,
            iterations,
            sends,
            recvs,
            dr_symmetric,
            dr_dh,
            spqr_symmetric,
            braid_add_epoch,
        ) = match.groups()
        candidate = {
            "ratchet_iterations": iterations,
            "sends": sends,
            "recvs": recvs,
            "dr_symmetric": dr_symmetric,
            "dr_dh": dr_dh,
            "spqr_symmetric": spqr_symmetric,
            "braid_add_epoch": braid_add_epoch,
        }
        current = metrics.get(benchmark)
        if current is None:
            metrics[benchmark] = candidate
            continue

        current_score = int(current["dr_symmetric"]) + int(current["spqr_symmetric"])
        candidate_score = int(candidate["dr_symmetric"]) + int(candidate["spqr_symmetric"])
        if candidate_score > current_score:
            metrics[benchmark] = candidate
    return metrics

def parse_file(path: Path, criterion_root: Path | None):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    results = []
    seen = set()
    ratchet_metrics = load_ratchet_metrics(lines)

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
                            metrics = load_criterion_metrics(criterion_root, target)
                            ratchets = ratchet_metrics.get(target, {})
                            results.append({
                                "file": path.name,
                                "benchmark": target,
                                "samples": metrics.get(
                                    "samples",
                                    find_samples_from_log(lines, max(i, j - 4), j),
                                ),
                                "measured_total": metrics.get("measured_total", ""),
                                "r_squared": metrics.get("r_squared", ""),
                                "low": fmt_2(low_val),
                                "low_unit": normalize_unit(low_unit),
                                "estimate": fmt_2(mid_val),
                                "estimate_unit": normalize_unit(mid_unit),
                                "high": fmt_2(high_val),
                                "high_unit": normalize_unit(high_unit),
                                "ratchet_iterations": ratchets.get("ratchet_iterations", ""),
                                "sends": ratchets.get("sends", ""),
                                "recvs": ratchets.get("recvs", ""),
                                "dr_symmetric": ratchets.get("dr_symmetric", ""),
                                "dr_dh": ratchets.get("dr_dh", ""),
                                "spqr_symmetric": ratchets.get("spqr_symmetric", ""),
                                "braid_add_epoch": ratchets.get("braid_add_epoch", ""),
                            })
                            seen.add(key)
                        break

            elif line.startswith(target) and "time:" in line:
                m = TIME_RE.search(line)
                if m:
                    low_val, low_unit, mid_val, mid_unit, high_val, high_unit = m.groups()
                    key = (path.name, target)
                    if key not in seen:
                        metrics = load_criterion_metrics(criterion_root, target)
                        ratchets = ratchet_metrics.get(target, {})
                        results.append({
                            "file": path.name,
                            "benchmark": target,
                            "samples": metrics.get(
                                "samples",
                                find_samples_from_log(lines, max(0, i - 4), i),
                            ),
                            "measured_total": metrics.get("measured_total", ""),
                            "r_squared": metrics.get("r_squared", ""),
                            "low": fmt_2(low_val),
                            "low_unit": normalize_unit(low_unit),
                            "estimate": fmt_2(mid_val),
                            "estimate_unit": normalize_unit(mid_unit),
                            "high": fmt_2(high_val),
                            "high_unit": normalize_unit(high_unit),
                            "ratchet_iterations": ratchets.get("ratchet_iterations", ""),
                            "sends": ratchets.get("sends", ""),
                            "recvs": ratchets.get("recvs", ""),
                            "dr_symmetric": ratchets.get("dr_symmetric", ""),
                            "dr_dh": ratchets.get("dr_dh", ""),
                            "spqr_symmetric": ratchets.get("spqr_symmetric", ""),
                            "braid_add_epoch": ratchets.get("braid_add_epoch", ""),
                        })
                        seen.add(key)

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--criterion-root", dest="criterion_root")
    args = parser.parse_args()

    criterion_root = Path(args.criterion_root) if args.criterion_root else None

    all_results = []
    for arg in args.files:
        all_results.extend(parse_file(Path(arg), criterion_root))

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "file",
            "benchmark",
            "samples",
            "measured_total",
            "r_squared",
            "low",
            "low_unit",
            "estimate",
            "estimate_unit",
            "high",
            "high_unit",
            "ratchet_iterations",
            "sends",
            "recvs",
            "dr_symmetric",
            "dr_dh",
            "spqr_symmetric",
            "braid_add_epoch",
        ]
    )
    writer.writeheader()
    writer.writerows(all_results)

if __name__ == "__main__":
    main()
