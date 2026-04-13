# signal-ratchet-bench

Benchmark orchestration repo for comparing:
- libsignal v0.73.3
- libsignal v0.92.1
- standalone SparsePostQuantumRatchet

This repo automates:
- cloning pinned upstream versions
- running the selected benchmark subset
- parsing raw benchmark logs
- computing median estimates
- writing a final Markdown summary to `output/summary.md`

Approximate runtime for a full run is about 10 minutes, depending on machine speed, available disk space, and whether dependencies are already built.

## What is being compared

The primary comparison is:
- `libsignal v0.73.3` as a pre-SPQR, Double Ratchet-era baseline
- `libsignal v0.92.1` as an SPQR-integrated, Triple Ratchet-era baseline

The repo also benchmarks standalone `SparsePostQuantumRatchet` as supporting subsystem evidence.

## Native usage

From the repo root, run:

bash run.sh

## Docker usage

Build:

docker build -t signal-ratchet-bench -f docker/Dockerfile .

Run:

docker run --rm -it -v "$PWD/output:/app/output" -v "$PWD/workspace:/app/workspace" signal-ratchet-bench

## Selected benchmark subset

Primary libsignal comparison includes only steady-state session benchmarks.

For libsignal v0.73.3:
- session encrypt
- session decrypt
- session encrypt+decrypt 1 way
- session encrypt+decrypt ping pong

For libsignal v0.92.1:
- encrypting on an existing chain
- decrypting on an existing chain
- session encrypt+decrypt 1 way
- session encrypt+decrypt ping pong

Standalone SPQR support includes:
- `benches/spqr.rs`
- `benches/chain.rs`

## Main outputs

After a successful run, the main files are:
- `output/v073_3/session_medians.csv`
- `output/v092_1/session_medians.csv`
- `output/spqr/spqr_medians.csv`
- `output/spqr/chain_medians.csv`
- `output/summary.md`

## Notes

- Benchmark timings depend on machine, load, OS, and toolchain.
- Docker is provided for environment reproducibility, but native runs are preferable for final timing fidelity.
- The scripts print high-level progress only; full benchmark logs are saved in `output/`.
