# Limitations & Responsible Use

- **Detection/monitoring only, non-kinetic.** Outputs are confidence-scored leads
  for lawful analysis and interdiction by partners — never targeting.
- **Synthetic benchmarks.** Metrics use planted ground truth; they measure
  algorithm correctness, not fielded accuracy on real imagery/AIS feeds.
- **Pattern-of-life anomaly detection trades precision for recall.** As the
  benchmark shows (R=1.0, P=0.6), it surfaces all planted anomalies but also
  benign off-pattern activity. Every hit requires analyst corroboration; an
  off-pattern observation has many innocent explanations.
- **Grid change detection depends on cell size and thresholds.** Too-coarse cells
  merge distinct activity; too-fine cells fragment it. Tune per AOI.
- **No real-imagery ingestion yet.** The pipeline consumes geolocated observation
  records; adapters for commercial imagery/AIS are post-prototype work.

Use only within your lawful authority (LICENSE §9, NOTICE).
