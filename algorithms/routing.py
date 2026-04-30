"""
Bus Routing Algorithms: Greedy and Dynamic Programming (TSP)
"""
import math
import time
import itertools
from typing import List, Tuple, Dict


def haversine_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    # p1, p2 are (lat, lng)
    R = 6371.0  # Earth radius in kilometers
    
    lat1, lon1 = p1
    lat2, lon2 = p2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def build_distance_matrix(stops: List[Dict]) -> List[List[float]]:
    n = len(stops)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                pi = (stops[i].get("lat", 0), stops[i].get("lng", 0))
                pj = (stops[j].get("lat", 0), stops[j].get("lng", 0))
                matrix[i][j] = haversine_distance(pi, pj)
    return matrix


# ─────────────────────────────────────────────
# GREEDY NEAREST NEIGHBOUR
# ─────────────────────────────────────────────
def greedy_route(stops: List[Dict], depot_index: int = 0) -> Dict:
    start_time = time.perf_counter()
    n = len(stops)
    dist = build_distance_matrix(stops)

    visited = [False] * n
    route = [depot_index]
    visited[depot_index] = True
    total_distance = 0.0

    current = depot_index
    for _ in range(n - 1):
        nearest = -1
        nearest_dist = float("inf")
        for j in range(n):
            if not visited[j] and dist[current][j] < nearest_dist:
                nearest_dist = dist[current][j]
                nearest = j
        route.append(nearest)
        visited[nearest] = True
        total_distance += nearest_dist
        current = nearest

    # Return to depot
    total_distance += dist[current][depot_index]
    route.append(depot_index)

    elapsed = (time.perf_counter() - start_time) * 1000  # ms

    return {
        "route": route,
        "total_distance": round(total_distance, 2),
        "time_ms": round(elapsed, 4),
        "algorithm": "Greedy (Nearest Neighbour)",
        "complexity": "O(n²)",
    }


# ─────────────────────────────────────────────
# DYNAMIC PROGRAMMING  (Held-Karp TSP)
# ─────────────────────────────────────────────
def dp_route(stops: List[Dict], depot_index: int = 0) -> Dict:
    start_time = time.perf_counter()
    n = len(stops)

    if n > 20:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "route": [],
            "total_distance": -1,
            "time_ms": round(elapsed, 4),
            "algorithm": "DP / Held-Karp",
            "complexity": "O(n² · 2ⁿ)",
            "error": f"Too many stops ({n}) for exact DP. Limit is 20.",
        }

    dist = build_distance_matrix(stops)

    INF = float("inf")
    # dp[S][i] = min cost to reach city i having visited exactly the cities in mask S
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    start_mask = 1 << depot_index
    dp[start_mask][depot_index] = 0.0

    for mask in range(size):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + dist[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    full_mask = size - 1
    best_cost = INF
    last = -1
    for u in range(n):
        if u == depot_index:
            continue
        cost = dp[full_mask][u] + dist[u][depot_index]
        if cost < best_cost:
            best_cost = cost
            last = u

    # Reconstruct path
    route = []
    mask = full_mask
    cur = last
    while cur != -1:
        route.append(cur)
        prev = parent[mask][cur]
        mask ^= (1 << cur)
        cur = prev
    route.reverse()
    route.append(depot_index)

    elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "route": route,
        "total_distance": round(best_cost, 2),
        "time_ms": round(elapsed, 4),
        "algorithm": "DP / Held-Karp (Optimal TSP)",
        "complexity": "O(n² · 2ⁿ)",
    }


# ─────────────────────────────────────────────
# COMPARISON HELPER
# ─────────────────────────────────────────────
def compare(stops: List[Dict], depot_index: int = 0) -> Dict:
    g = greedy_route(stops, depot_index)
    d = dp_route(stops, depot_index)
    improvement = None
    if d.get("total_distance", -1) > 0 and g["total_distance"] > 0:
        improvement = round(
            ((g["total_distance"] - d["total_distance"]) / g["total_distance"]) * 100, 2
        )
    return {"greedy": g, "dp": d, "improvement_percent": improvement}
