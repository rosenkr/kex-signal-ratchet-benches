# Benchmark summary

Raw logs and parsed single-run values are stored under `output/`.

## Comparison of libsignal v0.73.3 and v0.92.1 

| v0.73.3 benchmark                 | v0.92.1 benchmark                 | v0.73.3 sampling                  | v0.73.3 measured total | v0.73.3 R² | v0.73.3 time                    | v0.73.3 sends/recvs | v0.73.3 DR DH | v0.92.1 sampling                | v0.92.1 measured total | v0.92.1 R² | v0.92.1 time                    | v0.92.1 sends/recvs | v0.92.1 DR DH | v0.92.1 Braid add_epoch |
| --------------------------------- | --------------------------------- | --------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ------------------------------- | ---------------------- | ---------- | ------------------------------- | ------------------- | ------------- | ----------------------- |
| session encrypt                   | encrypting on an existing chain   | 100 samples, 1,040,300 iterations | 4.92 s                 | 0.51       | [4.64 µs 4.74 µs 4.85 µs]       | 2088875 / 0         | 0             | 100 samples, 429,250 iterations | 5.01 s                 | 0.38       | [11.44 µs 11.77 µs 12.11 µs]    | 691393 / 0          | 0             | 0                       |
| session decrypt                   | decrypting on an existing chain   | 100 samples, 808,000 iterations   | 5.11 s                 | 0.59       | [6.22 µs 6.34 µs 6.48 µs]       | 0 / 1332287         | 0             | 100 samples, 459,550 iterations | 5.10 s                 | 0.63       | [10.77 µs 10.94 µs 11.13 µs]    | 0 / 983837          | 0             | 0                       |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 100 samples, 530,250 iterations   | 5.40 s                 | 0.49       | [10.04 µs 10.31 µs 10.59 µs]    | 1054537 / 1054537   | 1             | 100 samples, 257,550 iterations | 5.89 s                 | 0.23       | [21.80 µs 22.47 µs 23.21 µs]    | 519693 / 519693     | 0             | 0                       |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 100 samples, 20,200 iterations    | 5.82 s                 | 0.44       | [278.53 µs 282.77 µs 287.58 µs] | 73166 / 73166       | 73166         | 100 samples, 15,150 iterations  | 5.83 s                 | 0.50       | [374.78 µs 388.31 µs 404.16 µs] | 46682 / 46682       | 46681         | 1073                    |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark        | Reported value           |
| ---------------- | ------------------------ |
| tests::send_recv | 35.68 µs/iter (+/- 9.56) |