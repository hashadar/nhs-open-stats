# nhs_stats_core

Optional Rust crate, exposed to Python through PyO3 and maturin. It currently holds two small functions
(`is_valid_ods_code`, `financial_year`) that mirror the Python behaviour, as a pattern for later hot paths.

```bash
cargo test                          # pure Rust, no Python needed
maturin develop --features python   # build the extension into the active virtualenv
```
