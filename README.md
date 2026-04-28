# signal-ratchet-bench

Benchmark orchestration repo for comparing:
- libsignal v0.73.3
- libsignal v0.92.1
- standalone SparsePostQuantumRatchet

This repo automates:
- cloning pinned upstream versions
- running the selected benchmark subset
- parsing raw benchmark logs
- writing a final Markdown summary to `output/summary.md`

Approximate runtime ~10-15 minutes

## What is being compared

The primary comparison is:
- `libsignal v0.73.3` as pre-SPQR, Double Ratchet
- `libsignal v0.92.1` as SPQR-integrated Double Ratchet, i.e. Triple Ratchet

The repo also benchmarks standalone `SparsePostQuantumRatchet`.

The only performance metric measured currently is execution time.

## Dependencies
Cargo, git and a protobuf compiler (protoc) are required to run.

## How to run

### Native
From the repo root, run: 
bash run.sh

### Docker

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
- `benches/spqr.rs` (public ratchet + symmetric ratchet, full spqr)
- `benches/chain.rs` (symmetric ratchet)

## Main outputs

After a successful run, the main file is:
- `output/summary.md`

While intermediate files are: 
- `output/v073_3/session_full.txt`
- `output/v073_3/session_values.csv`
- `output/v092_1/session_full.txt`
- `output/v092_1/session_values.csv`
- `output/spqr/spqr_full.txt`
- `output/spqr/spqr_values.csv`
- `output/spqr/chain_full.txt`
- `output/spqr/chain_values.csv`

The `session_values.csv` files include Criterion's reported sample count, actual total measured sample time, `R²`, and the reported timing interval.
