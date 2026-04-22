# Benchmark summary

## Comparison of libsignal v0.73.3 and v0.92.1 

| v0.73.3 benchmark                 | v0.92.1 benchmark                 | v0.73.3 median | v0.92.1 median | Median abs diff | % difference | v0.73.3 mean | v0.92.1 mean | Mean abs diff | v0.73.3 variance | v0.92.1 variance | Variance abs diff |
| --------------------------------- | --------------------------------- | -------------- | -------------- | --------------- | ------------ | ------------ | ------------ | ------------- | ---------------- | ---------------- | ----------------- |
| session encrypt                   | encrypting on an existing chain   | 2.99 µs        | 7.97 µs        | +4.98 µs        | +166.77%     | 2.94 µs      | 8.12 µs      | +5.18 µs      | 0.01 µs²         | 0.14 µs²         | +0.13 µs²         |
| session decrypt                   | decrypting on an existing chain   | 4.13 µs        | 7.16 µs        | +3.03 µs        | +73.27%      | 4.04 µs      | 7.37 µs      | +3.33 µs      | 0.03 µs²         | 0.15 µs²         | +0.12 µs²         |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 6.36 µs        | 14.32 µs       | +7.96 µs        | +125.12%     | 6.27 µs      | 14.14 µs     | +7.87 µs      | 0.03 µs²         | 0.20 µs²         | +0.17 µs²         |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 192.15 µs      | 255.28 µs      | +63.13 µs       | +32.85%      | 193.87 µs    | 255.88 µs    | +62.01 µs     | 9.86 µs²         | 62.84 µs²        | +52.98 µs²        |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark              | Median        | Mean          | Variance         |
| ---------------------- | ------------- | ------------- | ---------------- |
| tests::init_a          | 0.70 µs/iter  | 0.70 µs/iter  | 0.00 (µs/iter)^2 |
| tests::init_b          | 0.91 µs/iter  | 0.90 µs/iter  | 0.00 (µs/iter)^2 |
| tests::long_chain_send | 6.85 µs/iter  | 6.75 µs/iter  | 0.04 (µs/iter)^2 |
| tests::send_recv       | 25.10 µs/iter | 25.26 µs/iter | 0.08 (µs/iter)^2 |