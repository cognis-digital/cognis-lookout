"""Label precision/recall/F1."""

from __future__ import annotations


def prf(pred_set, truth_set) -> dict:
    pred, truth = set(pred_set), set(truth_set)
    tp, fp, fn = len(pred & truth), len(pred - truth), len(truth - pred)
    p = tp / (tp + fp) if (tp + fp) else 1.0
    r = tp / (tp + fn) if (tp + fn) else 1.0
    f = (2 * p * r / (p + r)) if (p + r) else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4)}
