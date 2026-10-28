"""Builds docs/data.json for the interactive views from the repository's CSV files.
The ten-economy values are the survey's Tables 3 and 4 (road network, daily road users, annotated frames);
DCR and the per-user rate are computed here, not typed."""
import csv, json, os, re

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# economy: road network (1000 km), daily road users urban/rural/express (millions), annotated frames (thousands), n datasets
ECON = [
    ("USA", 6685, (120, 48, 72), 641, 6), ("China", 5196, (320, 192, 128), 281, 5), ("India", 6371, (210, 189, 21), 94, 4),
    ("Japan", 1218, (51, 11, 11), 0, 0), ("Germany", 645, (34, 11, 12), 125, 4), ("UK", 418, (33, 7, 7), 0.5, 2),
    ("France", 1093, (30, 10, 11), 25, 1), ("Brazil", 1757, (62, 31, 10), 0, 0), ("Canada", 1042, (16, 5, 6), 7, 1),
    ("S. Korea", 114, (28, 5, 5), 230, 3)]
econ = []
for name, km, users, frames, n in ECON:
    u = sum(users)
    econ.append({"name": name, "roadKm": km * 1000, "users": u, "frames": frames * 1000, "n": n,
                 "dcr": frames * 1000 / km if km else 0, "perMillion": frames * 1000 / u, "ukBound": name == "UK"})

REGION = {"USA": "USA", "USA + SG": "USA", "Germany": "Germany", "China": "China", "India": "India", "S. Korea": "South Korea",
          "UK": "Other Europe", "France": "Other Europe", "Switzerland": "Other Europe", "Netherlands": "Other Europe", "Multi (EU)": "Other Europe",
          "Canada": "Canada", "S. Africa": "Africa", "MENA+EU": "Middle East and Europe", "Global": "Multi-region or global",
          "Multi": "Multi-region or global", "Synthetic": "Synthetic"}
FAMILY = {"Semantic Segmentation": "Camera scene understanding", "Night & Low-Visibility": "Camera scene understanding",
          "OOD & Anomaly Detection": "Camera scene understanding", "Adverse Conditions & Domain Shift": "Adverse conditions",
          "Thermal & Multispectral": "Camera scene understanding", "Event Camera": "Camera scene understanding",
          "Historical & Specialised Tasks": "Camera scene understanding", "3D Object Detection & LiDAR Segmentation": "3D detection and radar",
          "4D Imaging Radar": "3D detection and radar", "Localisation & SLAM": "Localisation", "Cooperative Perception (V2X)": "Cooperative and infrastructure",
          "Infrastructure & Fleet Cameras": "Cooperative and infrastructure", "Off-road & Unstructured": "Unstructured and Global South",
          "Global South & Unstructured": "Unstructured and Global South", "Motion Forecasting & Trajectory Prediction": "Forecasting",
          "Drone-based & Interactive Trajectories": "Forecasting", "Mixed-Traffic Trajectory Prediction": "Unstructured and Global South",
          "Closed-loop Control & Planning": "Closed-loop control", "Closed-loop Simulation Benchmarks": "Closed-loop control",
          "End-to-End Driving Logs & Benchmarks": "Closed-loop control"}
ds = []
for r in csv.DictReader(open(os.path.join(root, "data", "datasets.csv"), encoding="utf-8")):
    ds.append({"name": r["dataset"], "year": r["year"], "region": REGION.get(r["region"], r["region"]), "rawRegion": r["region"],
               "family": FAMILY[r["task"]], "pillar": r["pillar"], "scale": r["scale"], "note": r["note"]})
mat = [dict(r) for r in csv.DictReader(open(os.path.join(root, "data", "maturity.csv"), encoding="utf-8"))]
json.dump({"economies": econ, "datasets": ds, "maturity": mat}, open(os.path.join(root, "docs", "data.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print(len(econ), "economies;", len(ds), "datasets;", len(mat), "maturity rows")
