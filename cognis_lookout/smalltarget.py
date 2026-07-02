"""Small / faint-target detection for wide-area search (e.g. a lost hiker as a
pixel or two against vast terrain, or a small object in overhead imagery).

Uses CA-CFAR (cell-averaging constant-false-alarm-rate): for each pixel, estimate
the local background from a ring of training cells (a guard band excludes the
target), then flag pixels whose contrast exceeds k sigma — the standard way to
find a point target in a cluttered background. Adjacent hits are clustered into
compact blobs; large blobs are treated as terrain features, not point targets.

Non-kinetic search leads. See docs/LIMITATIONS.md.
An image is a 2-D list of intensity values (rows x cols).
"""

from __future__ import annotations

import statistics


def ca_cfar(image, guard: int = 1, train: int = 4, k: float = 5.0) -> list:
    H = len(image)
    W = len(image[0]) if H else 0
    hits = []
    span = guard + train
    for r in range(H):
        for c in range(W):
            vals = []
            for dr in range(-span, span + 1):
                for dc in range(-span, span + 1):
                    if abs(dr) <= guard and abs(dc) <= guard:
                        continue
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < H and 0 <= cc < W:
                        vals.append(image[rr][cc])
            if len(vals) < 8:
                continue
            mean = sum(vals) / len(vals)
            std = statistics.pstdev(vals)
            if std <= 0:
                continue
            snr = (image[r][c] - mean) / std
            if snr >= k:
                hits.append((r, c, snr))
    return hits


def _cluster(hits) -> list:
    snr_at = {(r, c): s for r, c, s in hits}
    seen, blobs = set(), []
    for start in snr_at:
        if start in seen:
            continue
        stack, comp = [start], []
        while stack:
            p = stack.pop()
            if p in seen or p not in snr_at:
                continue
            seen.add(p)
            comp.append(p)
            pr, pc = p
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    q = (pr + dr, pc + dc)
                    if q in snr_at and q not in seen:
                        stack.append(q)
        rows = [p[0] for p in comp]
        cols = [p[1] for p in comp]
        blobs.append({"row": round(sum(rows) / len(rows), 2),
                      "col": round(sum(cols) / len(cols), 2),
                      "size": len(comp),
                      "peak_snr": round(max(snr_at[p] for p in comp), 2)})
    return blobs


def detect_small_targets(image, k: float = 5.0, guard: int = 1, train: int = 4,
                         max_size: int = 8) -> list:
    blobs = [b for b in _cluster(ca_cfar(image, guard, train, k)) if b["size"] <= max_size]
    for b in blobs:
        b["confidence"] = round(min(0.99, (b["peak_snr"] / (k * 2)) *
                                    (1.0 / (1 + 0.15 * (b["size"] - 1)))), 4)
    blobs.sort(key=lambda b: -b["confidence"])
    return blobs


def to_geojson(blobs, geotransform) -> dict:
    gt = geotransform
    feats = []
    for b in blobs:
        lat = gt["origin_lat"] + b["row"] * gt["dlat"]
        lon = gt["origin_lon"] + b["col"] * gt["dlon"]
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
                      "properties": {"kind": "possible-person-or-object",
                                     "peak_snr": b["peak_snr"], "confidence": b["confidence"],
                                     "size_px": b["size"]}})
    return {"type": "FeatureCollection", "features": feats}
