# 🚌 Bus Route Optimizer

A professional web mapping tool for optimized bus routing using **Greedy** and **Dynamic Programming (Held-Karp)** algorithms. This application features a fully interactive map, geospatial address searching, and real-world geodesic distance calculations. Developed as part of a CCC project.

---

## 🚀 Features

- **Interactive Map Interface**: Built with Leaflet.js for a professional geospatial experience.
- **Location Searching**: Integrated Geocoder for easy address lookup and marker placement.
- **Toggleable Base Layers**: Switch seamlessly between standard Street Map and Satellite views.
- **Geodesic Distances**: Employs the Haversine formula to calculate accurate, real-world kilometer distances accounting for Earth's curvature.
- **Undo Functionality**: Easy route stop management with an intuitive undo feature.
- **Algorithm Comparison**: Side-by-side performance metrics comparing the Greedy heuristic vs. optimal Dynamic Programming.
- **Depot Selection**: Choose any added stop to serve as the starting bus depot.

---

## 📁 Project Structure

```text
bus_routing/
├── app.py                    # Flask web server backend
├── demo.py                   # CLI algorithm demonstration
├── requirements.txt          # Python dependencies
├── algorithms/
│   ├── __init__.py
│   └── routing.py            # Greedy & DP (Held-Karp) algorithms with Haversine logic
├── static/
│   ├── css/style.css         # UI styling
│   └── js/app.js             # Leaflet.js interactive map and frontend logic
├── templates/
│   └── index.html            # Main web interface
└── tests/
    └── test_routing.py       # Unit test suite
```

---

## 🛠️ How to Run

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```
*(If you do not have a requirements file, `pip install flask` is sufficient).*

### 2. Start the Web Application
```bash
python app.py
```
Open **http://localhost:5000** in your web browser.

### 3. Run the CLI Demo (Optional)
To test the routing algorithms purely in the terminal:
```bash
python demo.py
```

### 4. Run Unit Tests
To validate the routing algorithms and Haversine calculations:
```bash
python tests/test_routing.py
```

---

## 🧠 Algorithms

### Greedy — Nearest Neighbour
- **Idea**: At each step, visit the closest unvisited stop.
- **Time Complexity**: O(n²)
- **Space Complexity**: O(n)
- **Pros**: Lightning fast, easily handles hundreds of stops.
- **Cons**: Not always optimal — can result in routes that are 20–25% longer than necessary.

### Dynamic Programming — Held-Karp (Optimal TSP)
- **Idea**: Uses bitmask DP to evaluate all possible route permutations and find the globally optimal sequence.
- **Time Complexity**: O(n² · 2ⁿ)
- **Space Complexity**: O(n · 2ⁿ)
- **Pros**: Mathematically guaranteed to find the absolute shortest route.
- **Cons**: Exponential space/time complexity — safely limited to ~20 stops before performance degrades.

---

## 📌 Notes

- Coordinates are processed as real Latitude/Longitude pairs.
- Distances are displayed in kilometers (km).
- DP calculation is hard-capped at 20 stops to prevent server timeouts and extreme memory usage.

---

## 📄 Project Report

[View the Project Report PDF](https://drive.google.com/file/d/1Jv1KvD1Hh57ltWluRC5B21_J0ApHT2G_/view?usp=drivesdk)
