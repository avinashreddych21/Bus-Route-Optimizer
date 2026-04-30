"""
Standalone CLI demo for Bus Routing Algorithms
Run: python demo.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from algorithms.routing import compare

stops = [
    {"x": 20, "y": 30, "label": "School A"},
    {"x": 50, "y": 15, "label": "Park Stop"},
    {"x": 75, "y": 35, "label": "Mall Gate"},
    {"x": 65, "y": 65, "label": "Hospital"},
    {"x": 35, "y": 70, "label": "Library"},
    {"x": 15, "y": 55, "label": "Station"},
]

print("=" * 55)
print("  Bus Routing Optimizer — Algorithm Demo")
print("=" * 55)
print(f"\nStops ({len(stops)}):")
for i, s in enumerate(stops):
    print(f"  [{i}] {s['label']}  ({s['x']}, {s['y']})")

result = compare(stops, depot_index=0)
g = result["greedy"]
d = result["dp"]

print(f"\n{'─'*55}")
print(f"  GREEDY (Nearest Neighbour)")
print(f"  Route     : {' → '.join(str(r) for r in g['route'])}")
print(f"  Distance  : {g['total_distance']} units")
print(f"  Time      : {g['time_ms']} ms")
print(f"  Complexity: {g['complexity']}")

print(f"\n{'─'*55}")
print(f"  DP / Held-Karp (Optimal)")
if d.get("error"):
    print(f"  ERROR: {d['error']}")
else:
    print(f"  Route     : {' → '.join(str(r) for r in d['route'])}")
    print(f"  Distance  : {d['total_distance']} units")
    print(f"  Time      : {d['time_ms']} ms")
    print(f"  Complexity: {d['complexity']}")

if result["improvement_percent"] is not None:
    imp = result["improvement_percent"]
    print(f"\n{'─'*55}")
    if imp > 0:
        print(f"  DP is {imp}% shorter than Greedy ✓")
    elif imp == 0:
        print(f"  Both algorithms found the same route!")
    else:
        print(f"  Greedy happened to match optimal (±{abs(imp)}%)")

print("=" * 55)
