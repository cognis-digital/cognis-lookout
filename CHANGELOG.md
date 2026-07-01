# Changelog

Adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-07-01

Initial public release.

### Added
- AOI grid binning + geospatial helpers — `grid`, `geo`.
- Change detection (new-activity hotspots between two windows) — `change`.
- Pattern-of-life profiling + anomaly detection — `patternoflife`.
- Geofence entry/dwell detection — `geofence`.
- Deterministic synthetic generators with planted ground truth — `synth`.
- CLI (`cognis-lookout`): `demo`, `change`, `pol`.
- Verification harness: change + pattern-of-life metrics + performance;
  results in `RESULTS.md`. 5 tests. CI across Python 3.9–3.13.
