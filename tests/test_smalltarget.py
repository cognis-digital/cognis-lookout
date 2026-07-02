from bench import evaluate
from cognis_lookout import synth
from cognis_lookout.smalltarget import detect_small_targets, to_geojson


def _matched(blobs, truth, tol=1.5):
    return sum(1 for (tr, tc) in truth
               if any(abs(b["row"] - tr) <= tol and abs(b["col"] - tc) <= tol for b in blobs))


def test_finds_faint_people_in_terrain():
    img, truth = synth.landscape_with_people()
    blobs = detect_small_targets(img, k=5.0)
    assert _matched(blobs, truth) == len(truth)      # recall = 1.0
    assert len(blobs) <= len(truth) + 2


def test_geojson_export():
    img, truth = synth.landscape_with_people(n_people=3)
    gt = {"origin_lat": 40.0, "origin_lon": -105.0, "dlat": -0.0005, "dlon": 0.0005}
    fc = to_geojson(detect_small_targets(img, k=5.0), gt)
    assert fc["type"] == "FeatureCollection" and fc["features"]
    assert fc["features"][0]["properties"]["kind"] == "possible-person-or-object"


def test_bench_small_target_recall():
    assert evaluate.evaluate()["small_target"]["recall"] >= 0.9
