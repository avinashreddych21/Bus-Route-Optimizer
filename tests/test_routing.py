"""Unit tests for routing algorithms."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms.routing import greedy_route, dp_route, compare, haversine_distance, build_distance_matrix

# ── Helper ──────────────────────────────────────────
def make_stops(coords):
    return [{"lat": lat, "lng": lng, "label": f"S{i}"} for i, (lat, lng) in enumerate(coords)]

# ── Tests ───────────────────────────────────────────
def test_haversine():
    # distance between same point is 0
    assert haversine_distance((1,1), (1,1)) == 0.0
    # distance 1 degree lat is ~111 km
    d = haversine_distance((0,0), (1,0))
    assert 110 < d < 112
    print("PASS  test_haversine")

def test_distance_matrix_symmetry():
    stops = make_stops([(0,0),(10,0),(5,5)])
    dm = build_distance_matrix(stops)
    assert dm[0][1] == dm[1][0]
    assert dm[0][0] == 0
    print("PASS  test_distance_matrix_symmetry")

def test_greedy_two_stops():
    stops = make_stops([(0,0),(10,0)])
    r = greedy_route(stops, 0)
    assert r["route"][0] == 0
    assert r["route"][-1] == 0
    # Two way trip: 10 degrees along equator is ~1113 km. Total ~2226 km
    d = haversine_distance((0,0), (10,0)) * 2
    assert r["total_distance"] == pytest_approx(d, rel=1e-2)
    print("PASS  test_greedy_two_stops")

def test_greedy_returns_all_stops():
    stops = make_stops([(0,0),(10,0),(5,8),(2,5)])
    r = greedy_route(stops, 0)
    visited = set(r["route"])
    assert visited == {0, 1, 2, 3}
    print("PASS  test_greedy_returns_all_stops")

def test_dp_optimal_triangle():
    stops = make_stops([(0,0),(10,0),(5, 8.66)])
    r = dp_route(stops, 0)
    assert r["total_distance"] > 0
    print("PASS  test_dp_optimal_triangle")

def test_dp_better_or_equal_greedy():
    stops = make_stops([(10,10),(80,10),(50,70),(20,50),(70,40)])
    g = greedy_route(stops, 0)
    d = dp_route(stops, 0)
    assert d["total_distance"] <= g["total_distance"] + 1e-6
    print("PASS  test_dp_better_or_equal_greedy")

def test_dp_limit():
    stops = make_stops([(i, i) for i in range(21)])  # 21 stops > limit
    r = dp_route(stops, 0)
    assert "error" in r
    print("PASS  test_dp_limit")

def test_compare_structure():
    stops = make_stops([(0,0),(50,0),(25,40)])
    result = compare(stops, 0)
    assert "greedy" in result and "dp" in result
    assert "improvement_percent" in result
    print("PASS  test_compare_structure")

def pytest_approx(val, rel=1e-4):
    class Approx:
        def __eq__(self, other):
            return abs(other - val) / max(abs(val), 1e-12) <= rel
    return Approx()

# ── Run ─────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        test_haversine,
        test_distance_matrix_symmetry,
        test_greedy_two_stops,
        test_greedy_returns_all_stops,
        test_dp_optimal_triangle,
        test_dp_better_or_equal_greedy,
        test_dp_limit,
        test_compare_structure,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*40}")
    print(f"Results: {len(tests)-failed}/{len(tests)} passed")
    if failed: sys.exit(1)
