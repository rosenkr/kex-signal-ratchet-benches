# Benchmark summary

Summary tables are rounded to two decimal places for readability. The underlying CSV outputs retain the computed values used to generate this report.

## Comparison of libsignal v0.73.3 and v0.92.1 

| v0.73.3 benchmark                 | v0.92.1 benchmark                 | v0.73.3 median | v0.92.1 median | Median abs diff | % difference | v0.73.3 mean | v0.92.1 mean | Mean abs diff | v0.73.3 variance | v0.92.1 variance | Variance abs diff |
| --------------------------------- | --------------------------------- | -------------- | -------------- | --------------- | ------------ | ------------ | ------------ | ------------- | ---------------- | ---------------- | ----------------- |
| session encrypt                   | encrypting on an existing chain   | 3.13 µs        | 7.54 µs        | +4.41 µs        | +140.91%     | 3.10 µs      | 7.32 µs      | +4.22 µs      | 0.02 µs²         | 0.14 µs²         | +0.12 µs²         |
| session decrypt                   | decrypting on an existing chain   | 4.50 µs        | 7.40 µs        | +2.90 µs        | +64.45%      | 4.40 µs      | 7.21 µs      | +2.81 µs      | 0.09 µs²         | 0.16 µs²         | +0.07 µs²         |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 6.99 µs        | 13.80 µs       | +6.81 µs        | +97.34%      | 7.10 µs      | 13.64 µs     | +6.54 µs      | 0.04 µs²         | 0.78 µs²         | +0.73 µs²         |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 196.44 µs      | 252.44 µs      | +56.00 µs       | +28.51%      | 196.55 µs    | 253.83 µs    | +57.28 µs     | 3.59 µs²         | 5.67 µs²         | +2.07 µs²         |

## Standalone SPQR (`benches/spqr.rs`)

These benchmarks are included as supporting evidence that SPQR-related operations have measurable cost. They support the hypothesis that SPQR may contribute to the higher cost observed in v0.92.1, but they do not by themselves prove that SPQR is the sole cause of the slowdown.

| Benchmark              | Median        | Mean          | Variance         |
| ---------------------- | ------------- | ------------- | ---------------- |
| tests::init_a          | 0.74 µs/iter  | 0.72 µs/iter  | 0.00 (µs/iter)^2 |
| tests::init_b          | 0.93 µs/iter  | 0.91 µs/iter  | 0.00 (µs/iter)^2 |
| tests::long_chain_send | 6.59 µs/iter  | 6.73 µs/iter  | 0.05 (µs/iter)^2 |
| tests::send_recv       | 25.58 µs/iter | 25.47 µs/iter | 0.09 (µs/iter)^2 |