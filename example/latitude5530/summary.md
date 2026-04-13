# Benchmark summary

## libsignal version comparison

| Old version                       | New version                       | Old median  | New median  | Absolute difference | % difference |
| --------------------------------- | --------------------------------- | ----------- | ----------- | ------------------- | ------------ |
| session encrypt                   | encrypting on an existing chain   | 2.7677 µs   | 6.8153 µs   | +4.0476 µs          | +146.24%     |
| session decrypt                   | decrypting on an existing chain   | 3.7719 µs   | 6.7229 µs   | +2.9510 µs          | +78.24%      |
| session encrypt+decrypt 1 way     | session encrypt+decrypt 1 way     | 5.9736 µs   | 12.4220 µs  | +6.4484 µs          | +107.95%     |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 171.5900 µs | 225.1900 µs | +53.6000 µs         | +31.24%      |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark              | Median          |
| ---------------------- | --------------- |
| tests::init_a          | 0.6736 µs/iter  |
| tests::init_b          | 0.9079 µs/iter  |
| tests::long_chain_send | 6.0889 µs/iter  |
| tests::send_recv       | 24.3475 µs/iter |

## Standalone SPQR chain (`benches/chain.rs`)

| Benchmark                 | Median         |
| ------------------------- | -------------- |
| tests::add_epoch          | 0.8143 µs/iter |
| tests::recv_key           | 0.5441 µs/iter |
| tests::recv_skip_key      | 1.0935 µs/iter |
| tests::recv_with_truncate | 1.0801 µs/iter |
| tests::send_key           | 0.5393 µs/iter |