"""Accuracy evaluation vs planted ground truth."""

from __future__ import annotations

import json

from cognis_lookout import synth
from cognis_lookout.change import detect_new_activity
from cognis_lookout.patternoflife import anomalies, build_profile

from .metrics import prf


def evaluate() -> dict:
    base, cur, planted_cells = synth.change_scenario()
    hotspots = detect_new_activity(base, cur, origin=synth.ORIGIN, cell_deg=synth.CELL)
    pred_cells = {tuple(h["cell"]) for h in hotspots}
    change_prf = prf(pred_cells, planted_cells)

    obs, planted_anoms = synth.pol_scenario()
    prof = build_profile(obs, origin=synth.ORIGIN, cell_deg=synth.CELL)
    an = anomalies(obs, prof, origin=synth.ORIGIN, cell_deg=synth.CELL)
    pred_anoms = {a["id"] for a in an}
    anomaly_prf = prf(pred_anoms, planted_anoms)

    determinism = ({tuple(h["cell"]) for h in
                    detect_new_activity(base, cur, origin=synth.ORIGIN, cell_deg=synth.CELL)}
                   == pred_cells)

    return {"change_detection": change_prf, "pattern_of_life": anomaly_prf,
            "hotspots": len(hotspots), "determinism": determinism}


def main():
    print(json.dumps(evaluate(), indent=2))


if __name__ == "__main__":
    main()
