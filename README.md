# signal-ratchet-bench

Benchmarks comparing libsignal v0.73.3 (Double Ratchet) vs v0.92.1 (Triple Ratchet / SPQR-integrated), plus standalone SparsePostQuantumRatchet. Approximate runtime: 10–15 minutes.

## What it does

1. **Sets up environment** — clones pinned upstream versions of libsignal and SPQR into `workspace/`
2. **Applies patches** — instruments the cloned source with ratchet operation counters (`[ratchet-counts]` output) needed for the summary
3. **Runs benchmarks** — steady-state session benchmarks on both libsignal versions; `spqr.rs` and `chain.rs` on standalone SPQR
4. **Parses and summarizes** — extracts Criterion metrics and ratchet counts into CSVs, then writes `output/summary.md`

## Dependencies

Cargo, git, protobuf compiler (`protoc`).

## Running

**Native:**
```
bash run.sh
```

**Docker:**
```
docker build -t kex-bench -f docker/Dockerfile .
docker run --rm -v "$(pwd)/output:/app/output" kex-bench
```

## Benchmark subset

Only steady-state session benchmarks are included (no setup/teardown noise).

| Version | Benchmarks |
|---|---|
| v0.73.3 | session encrypt, session decrypt, encrypt+decrypt 1 way, encrypt+decrypt ping pong |
| v0.92.1 | encrypting on an existing chain, decrypting on an existing chain, encrypt+decrypt 1 way, encrypt+decrypt ping pong |
| SPQR standalone | `benches/spqr.rs` (full SPQR)

## Output
An example summary is in `example/`.
