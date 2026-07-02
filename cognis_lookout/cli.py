"""Cognis Lookout CLI."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__, synth
from .change import detect_new_activity
from .grid import load_observations
from .patternoflife import anomalies, build_profile
from .report import render_json, render_text


def cmd_demo(args):
    base, cur, _ = synth.change_scenario()
    obs, _ = synth.pol_scenario()
    prof = build_profile(obs)
    product = {"new_activity": detect_new_activity(base, cur),
               "anomalies": anomalies(obs, prof)}
    print(render_text(product))
    return 0


def cmd_change(args):
    base = load_observations(args.baseline)
    cur = load_observations(args.current)
    out = detect_new_activity(base, cur)
    print(json.dumps(out, indent=2))
    return 0


def cmd_pol(args):
    obs = load_observations(args.observations)
    prof = build_profile(obs)
    print(json.dumps(anomalies(obs, prof), indent=2))
    return 0


def cmd_search(args):
    """Wide-area small-target search — e.g. a lost hiker as a pixel in terrain."""
    from . import synth
    from .smalltarget import detect_small_targets
    img, truth = synth.landscape_with_people()
    blobs = detect_small_targets(img, k=args.k)
    print(f"COGNIS LOOKOUT | wide-area search over {len(img)}x{len(img[0])} terrain scene (CA-CFAR)")
    print(f"planted targets: {len(truth)}   detections: {len(blobs)}   (k={args.k} sigma)")
    for i, b in enumerate(blobs[:10], 1):
        print(f"  [{i}] pixel ({b['row']},{b['col']}) size={b['size']}px "
              f"SNR={b['peak_snr']} conf={b['confidence']:.2f}")
    print("NOTE: non-kinetic search leads (possible person/object); corroborate before tasking.")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="cognis-lookout",
                                description="Cognis Lookout — geospatial change & pattern-of-life (non-kinetic)")
    p.add_argument("--version", action="version", version=f"cognis-lookout {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("demo", help="end-to-end demo on synthetic data")
    d.set_defaults(func=cmd_demo)

    c = sub.add_parser("change", help="new-activity change detection between two windows")
    c.add_argument("--baseline", required=True)
    c.add_argument("--current", required=True)
    c.set_defaults(func=cmd_change)

    pol = sub.add_parser("pol", help="pattern-of-life anomaly detection")
    pol.add_argument("--observations", required=True)
    pol.set_defaults(func=cmd_pol)

    s = sub.add_parser("search", help="wide-area small-target search (lost hiker/object)")
    s.add_argument("--k", type=float, default=5.0, help="CFAR threshold (sigma)")
    s.set_defaults(func=cmd_search)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
