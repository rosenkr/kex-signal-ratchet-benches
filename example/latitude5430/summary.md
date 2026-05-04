# Benchmark summary

Raw logs and parsed single-run values are stored under `output/`.

## Comparison of libsignal v0.73.3 and v0.92.1 

| v0.73.3 benchmark                 | v0.92.1 benchmark                 | v0.73.3 sampling                  | v0.73.3 measured total | v0.73.3 R² | v0.73.3 time                    | v0.73.3 sends/recvs | v0.73.3 DR DH | v0.92.1 sampling                | v0.92.1 measured total | v0.92.1 R² | v0.92.1 time                    | v0.92.1 sends/recvs | v0.92.1 DR DH | v0.92.1 Braid add_epoch |
| --------------------------------- | --------------------------------- | --------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ----------------------- |
| session encrypt                   | encrypting on an existing chain   | 100 samples, 1,509,950 iterations | 4.99 s                 | 0.97       | [3.28 µs 3.30 µs 3.31 µs]       | 2558525 / 0         | 0             | 100 samples, 469,650 iterations | 4.73 s                 | 0.98       | [10.02 µs 10.05 µs 10.08 µs]    | 993937 / 0          | 0             | 0                       |
| session decrypt                   | decrypting on an existing chain   | 100 samples, 1,111,000 iterations | 5.00 s                 | 0.98       | [4.48 µs 4.50 µs 4.51 µs]       | 0 / 2159575         | 0             | 100 samples, 575,700 iterations | 4.94 s                 | 0.89       | [8.44 µs 8.50 µs 8.56 µs]       | 0 / 1099987         | 0             | 0                       |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 100 samples, 717,100 iterations   | 4.93 s                 | 0.95       | [6.84 µs 6.87 µs 6.90 µs]       | 1241387 / 1241387   | 1             | 100 samples, 318,150 iterations | 4.86 s                 | 0.95       | [15.12 µs 15.18 µs 15.25 µs]    | 580293 / 580293     | 0             | 0                       |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 100 samples, 25,250 iterations    | 5.35 s                 | 0.98       | [211.16 µs 211.72 µs 212.29 µs] | 83266 / 83266       | 83266         | 100 samples, 20,200 iterations  | 5.42 s                 | 0.99       | [267.24 µs 267.63 µs 268.08 µs] | 73166 / 73166       | 73165         | 1682                    |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark        | Reported value           |
| ---------------- | ------------------------ |
| tests::send_recv | 26.98 µs/iter (+/- 1.36) |
