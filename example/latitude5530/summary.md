# Benchmark summary

## libsignal version comparison

| Old version | New version | Old median | New median | Absolute difference | % difference |
|---|---|---|---|---|---|
| session encrypt | encrypting on an existing chain | 2.7772 µs | 7.3105 µs | +4.5333 µs | +163.23% |
| session decrypt | decrypting on an existing chain | 3.7174 µs | 6.7042 µs | +2.9868 µs | +80.35% |
| session encrypt+decrypt 1 way | session encrypt+decrypt 1 way | 5.8667 µs | 12.1310 µs | +6.2643 µs | +106.78% |
| session encrypt+decrypt ping pong | session encrypt+decrypt ping pong | 173.0500 µs | 220.0100 µs | +46.9600 µs | +27.14% |

## Standalone SPQR (`benches/spqr.rs`)

| Benchmark | Median |
|---|---|
| tests::init_a | 664.85 ns/iter |
| tests::init_b | 837.51 ns/iter |
| tests::long_chain_send | 5927.91 ns/iter |
| tests::send_recv | 23122.85 ns/iter |

## Standalone SPQR chain (`benches/chain.rs`)

| Benchmark | Median |
|---|---|
| tests::add_epoch | 756.96 ns/iter |
| tests::recv_key | 496.92 ns/iter |
| tests::recv_skip_key | 997.33 ns/iter |
| tests::recv_with_truncate | 985.86 ns/iter |
| tests::send_key | 494.60 ns/iter |