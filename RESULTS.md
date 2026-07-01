# Cognis Lookout — Verification Results

Reproduce with: `python bench/run_all.py`.

Environment: CPython 3.14.0 on Windows/AMD64. Deterministic synthetic data; detection/monitoring only.

| Metric | Value |
|---|---|
| Change detection (new activity) | P=1.000 / R=1.000 / F1=1.000 |
| Pattern-of-life anomaly | P=0.600 / R=1.000 / F1=0.750 |
| Determinism | True |

## Performance (single-thread, stdlib only)

| Observations | Detect (s) | Obs/s |
|---:|---:|---:|
| 2,400 | 0.0023 | 1,039,771 |
| 12,000 | 0.0102 | 1,181,079 |
| 48,000 | 0.0381 | 1,259,713 |

Gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md`.
