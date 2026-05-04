# Benchmark summary

Raw logs and parsed single-run values are stored under `output/`.

## Comparison of libsignal v0.73.3 and v0.92.1 

| v0.73.3 benchmark                 | v0.92.1 benchmark                 | v0.73.3 sampling                  | v0.73.3 measured total | v0.73.3 R² | v0.73.3 time                    | v0.73.3 sends/recvs | v0.73.3 DR DH | v0.92.1 sampling                | v0.92.1 measured total | v0.92.1 R² | v0.92.1 time                    | v0.92.1 sends/recvs | v0.92.1 DR DH | v0.92.1 Braid add_epoch |
| --------------------------------- | --------------------------------- | --------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ----------------------- |
| session encrypt                   | encrypting on an existing chain   | 100 samples, 1,797,800 iterations | 5.02 s                 | 0.97       | [2.78 µs 2.79 µs 2.81 µs]       | 3894951 / 0         | 0             | 100 samples, 530,250 iterations | 4.72 s                 | 0.30       | [8.57 µs 8.82 µs 9.12 µs]       | 1054537 / 0         | 0             | 0                       |
| session decrypt                   | decrypting on an existing chain   | 100 samples, 1,222,100 iterations | 4.93 s                 | 1.00       | [4.03 µs 4.03 µs 4.04 µs]       | 0 / 2270675         | 0             | 100 samples, 570,650 iterations | 5.08 s                 | 0.58       | [8.78 µs 8.93 µs 9.11 µs]       | 0 / 1094937         | 0             | 0                       |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 100 samples, 787,800 iterations   | 4.96 s                 | 0.93       | [6.26 µs 6.29 µs 6.34 µs]       | 1312087 / 1312087   | 1             | 100 samples, 318,150 iterations | 5.45 s                 | 0.45       | [16.64 µs 16.93 µs 17.27 µs]    | 580293 / 580293     | 0             | 0                       |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 100 samples, 30,300 iterations    | 5.61 s                 | 0.92       | [184.18 µs 185.21 µs 186.51 µs] | 93366 / 93366       | 93366         | 100 samples, 20,200 iterations  | 6.23 s                 | 0.36       | [301.30 µs 308.44 µs 317.11 µs] | 73166 / 73166       | 73165         | 1682                    |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark        | Reported value           |
| ---------------- | ------------------------ |
| tests::send_recv | 23.99 µs/iter (+/- 2.11) |