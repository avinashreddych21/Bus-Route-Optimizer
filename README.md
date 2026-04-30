# 🚌 Bus Routing & Student Drop-off System

Optimized bus routing using **Greedy** and **Dynamic Programming** algorithms.

---

## 📁 Project Structure

```
bus_routing/
├── app.py                    # Flask web server
├── demo.py                   # CLI algorithm demo
├── requirements.txt
├── algorithms/
│   ├── __init__.py
│   └── routing.py            # Greedy & DP (Held-Karp) algorithms
├── static/
│   ├── css/style.css
│   └── js/app.js             # Interactive map UI
├── templates/
│   └── index.html
└── tests/
    └── test_routing.py       # Unit tests
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the web app
```bash
python app.py
```
Open **http://localhost:5000** in your browser.

### 3. Run the CLI demo
```bash
python demo.py
```

### 4. Run unit tests
```bash
python tests/test_routing.py
```

---

## 🧠 Algorithms

### Greedy — Nearest Neighbour
- **Idea**: At each step, visit the closest unvisited stop.
- **Time Complexity**: O(n²)
- **Pros**: Very fast, easy to implement.
- **Cons**: Not always optimal — can be 20–25% worse.

### Dynamic Programming — Held-Karp (Optimal TSP)
- **Idea**: Use bitmask DP to evaluate all subsets of stops and find the globally optimal route.
- **Time Complexity**: O(n² · 2ⁿ)
- **Pros**: Guaranteed optimal route.
- **Cons**: Exponential space/time — limited to ~20 stops.

### Key Formula (Held-Karp)
```
dp[S][i] = min cost to reach node i having visited exactly the nodes in bitmask S
dp[S | (1<<v)][v] = min(dp[S][u] + dist[u][v])  for all u in S
```

---

## 🖥 Web Interface Features

| Feature | Description |
|---------|-------------|
| **Click to add stops** | Click anywhere on the canvas |
| **Presets** | Load 6, 10, or 15 stop configurations |
| **Run Greedy** | Visualise nearest-neighbour route (yellow) |
| **Run DP** | Visualise optimal Held-Karp route (green) |
| **Compare Both** | Side-by-side metrics + improvement % |
| **Depot selection** | Choose any stop as the starting bus depot |

---

## 📊 Complexity Comparison

| Algorithm | Time | Space | Optimality |
|-----------|------|-------|------------|
| Greedy    | O(n²) | O(n) | Near-optimal |
| DP (Held-Karp) | O(n²·2ⁿ) | O(n·2ⁿ) | **Optimal** |

---

## 📌 Notes
- DP is limited to **≤ 20 stops** due to exponential complexity.
- Coordinates are normalised to a 0–100 grid (percentage of canvas size).
- Distances are Euclidean (straight-line).
