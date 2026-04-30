// ── State ──────────────────────────────────────────────
const state = {
  stops: [],          // [{lat,lng,label}]
  greedyRoute: null,
  dpRoute: null,
  busMarker: null,
  animFrame: null
};

// ── Initialize Map ─────────────────────────────────────
const map = L.map('map-canvas').setView([51.505, -0.09], 13);

const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
});

const satelliteLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    attribution: 'Map data © Google'
});

osmLayer.addTo(map);

const baseMaps = {
    "Map View": osmLayer,
    "Satellite View": satelliteLayer
};
L.control.layers(baseMaps).addTo(map);

// Add Geocoder Search Control
L.Control.geocoder({
  defaultMarkGeocode: false
})
.on('markgeocode', function(e) {
  const latlng = e.geocode.center;
  map.setView(latlng, map.getZoom() || 13);
})
.addTo(map);

const markersGroup = L.layerGroup().addTo(map);
const routesGroup = L.layerGroup().addTo(map);

// ── Click to add stop ──────────────────────────────────
map.on("click", (e) => {
  state.stops.push({ lat: e.latlng.lat, lng: e.latlng.lng, label: `S${state.stops.length}` });
  clearRoutes();
  updateStopList();
  drawMap();
});

// ── Preset stops ───────────────────────────────────────
const PRESETS = {
  6: [
    {lat: 51.515, lng: -0.10}, {lat: 51.505, lng: -0.09}, {lat: 51.510, lng: -0.11},
    {lat: 51.495, lng: -0.08}, {lat: 51.520, lng: -0.07}, {lat: 51.500, lng: -0.12}
  ],
  10: [
    {lat: 51.515, lng: -0.10}, {lat: 51.505, lng: -0.09}, {lat: 51.510, lng: -0.11},
    {lat: 51.495, lng: -0.08}, {lat: 51.520, lng: -0.07}, {lat: 51.500, lng: -0.12},
    {lat: 51.525, lng: -0.10}, {lat: 51.490, lng: -0.09}, {lat: 51.508, lng: -0.06},
    {lat: 51.498, lng: -0.11}
  ],
  15: [
    {lat: 51.515, lng: -0.10}, {lat: 51.505, lng: -0.09}, {lat: 51.510, lng: -0.11},
    {lat: 51.495, lng: -0.08}, {lat: 51.520, lng: -0.07}, {lat: 51.500, lng: -0.12},
    {lat: 51.525, lng: -0.10}, {lat: 51.490, lng: -0.09}, {lat: 51.508, lng: -0.06},
    {lat: 51.498, lng: -0.11}, {lat: 51.530, lng: -0.08}, {lat: 51.485, lng: -0.07},
    {lat: 51.512, lng: -0.13}, {lat: 51.522, lng: -0.12}, {lat: 51.488, lng: -0.10}
  ]
};

function loadPreset(n) {
  state.stops = PRESETS[n].map((p, i) => ({ ...p, label: `S${i}` }));
  clearRoutes();
  updateStopList();
  
  if (state.stops.length > 0) {
      const bounds = L.latLngBounds(state.stops.map(s => [s.lat, s.lng]));
      map.fitBounds(bounds, { padding: [50, 50] });
  }
  
  drawMap();
}

function clearAll() {
  state.stops = [];
  clearRoutes();
  updateStopList();
  drawMap();
  document.getElementById("results-panel").classList.add("hidden");
}

function clearRoutes() {
  state.greedyRoute = null;
  state.dpRoute = null;
  if (state.animFrame) cancelAnimationFrame(state.animFrame);
  if (state.busMarker) {
      map.removeLayer(state.busMarker);
      state.busMarker = null;
  }
}

function undoLastStop() {
  if (state.stops.length > 0) {
    state.stops.pop();
    clearRoutes();
    updateStopList();
    drawMap();
  }
}

// ── Stop list UI ───────────────────────────────────────
function updateStopList() {
  const depot = +document.getElementById("depot-input").value || 0;
  const list  = document.getElementById("stop-list");
  list.innerHTML = state.stops.map((s, i) => `
    <div class="stop-item ${i === depot ? 'depot' : ''}">
      <span class="dot"></span>
      <span class="idx">#${i}</span>
      <span>${s.label} &nbsp;(${s.lat.toFixed(4)}, ${s.lng.toFixed(4)})</span>
      ${i === depot ? '<span style="margin-left:auto;font-size:0.7rem;color:var(--depot)">DEPOT</span>' : ''}
    </div>
  `).join("");
}

document.getElementById("depot-input").addEventListener("input", () => {
  updateStopList();
  drawMap();
});

// ── Draw Map ───────────────────────────────────────────
function drawMap() {
  markersGroup.clearLayers();
  routesGroup.clearLayers();

  const depot = +document.getElementById("depot-input").value || 0;

  // Draw routes
  if (state.greedyRoute) drawRoute(state.greedyRoute, "#f7b731", 4, []);
  if (state.dpRoute)     drawRoute(state.dpRoute,     "#26de81", 4, [10, 5]);

  // Draw stops
  state.stops.forEach((s, i) => {
    const isDepot = i === depot;
    const color = isDepot ? "#ff9f43" : "#a29bfe";
    const radius = isDepot ? 8 : 6;

    const marker = L.circleMarker([s.lat, s.lng], {
        radius: radius,
        color: isDepot ? "#fff" : "rgba(255,255,255,0.5)",
        weight: isDepot ? 2 : 1,
        fillColor: color,
        fillOpacity: 1
    }).addTo(markersGroup);

    marker.bindTooltip(isDepot ? "🏠 " + s.label : i + "", {
        permanent: true,
        direction: "top",
        className: isDepot ? "depot-label" : "stop-label"
    });
  });
}

function drawRoute(route, color, weight, dashArray) {
  if (!route || route.length < 2) return;
  const coords = route.map(idx => {
      const s = state.stops[idx];
      return [s.lat, s.lng];
  });

  L.polyline(coords, {
      color: color,
      weight: weight,
      dashArray: dashArray,
      opacity: 0.8
  }).addTo(routesGroup);
}

// ── Bus Animation ──────────────────────────────────────
function animateBus(routeIndices) {
  if (state.animFrame) cancelAnimationFrame(state.animFrame);
  if (state.busMarker) map.removeLayer(state.busMarker);

  if (!routeIndices || routeIndices.length < 2) return;

  const coords = routeIndices.map(idx => {
      const s = state.stops[idx];
      return [s.lat, s.lng];
  });

  const busIcon = L.divIcon({
      html: '🚌',
      className: 'bus-marker',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
  });

  state.busMarker = L.marker(coords[0], { icon: busIcon }).addTo(map);

  let segment = 0;
  let progress = 0;
  let lastTime = null;
  const speed = 0.0015; // Animation speed

  function step(time) {
      if (!lastTime) lastTime = time;
      const dt = time - lastTime;
      lastTime = time;

      progress += speed * dt;

      if (progress >= 1) {
          progress = 0;
          segment++;
      }

      if (segment >= coords.length - 1) {
          state.busMarker.setLatLng(coords[coords.length - 1]);
          return;
      }

      const p1 = coords[segment];
      const p2 = coords[segment + 1];

      const lat = p1[0] + (p2[0] - p1[0]) * progress;
      const lng = p1[1] + (p2[1] - p1[1]) * progress;

      state.busMarker.setLatLng([lat, lng]);

      state.animFrame = requestAnimationFrame(step);
  }

  state.animFrame = requestAnimationFrame(step);
}

// ── API calls ──────────────────────────────────────────
async function runAlgorithm(type) {
  if (state.stops.length < 2) {
    showError("Add at least 2 stops first!");
    return;
  }
  const depot = +document.getElementById("depot-input").value || 0;
  if (depot >= state.stops.length) {
    showError("Depot index out of range!");
    return;
  }

  setLoading(true);

  try {
    const res = await fetch(`/api/${type}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ stops: state.stops, depot }),
    });
    const data = await res.json();

    if (data.error) { showError(data.error); setLoading(false); return; }

    drawMap();
    if (type === "greedy") {
      state.greedyRoute = data.route;
      state.dpRoute = null;
      showSingleResult(data, "greedy");
      animateBus(state.greedyRoute);
    } else if (type === "dp") {
      state.dpRoute = data.route;
      state.greedyRoute = null;
      showSingleResult(data, "dp");
      animateBus(state.dpRoute);
    } else {
      state.greedyRoute = data.greedy.route;
      state.dpRoute     = data.dp.route;
      showCompareResult(data);
      animateBus(state.dpRoute || state.greedyRoute);
    }
  } catch (e) {
    showError("Server error: " + e.message);
  }
  setLoading(false);
}

function setLoading(on) {
  document.querySelectorAll(".btn").forEach(b => b.disabled = on);
  if (on) {
    const p = document.getElementById("results-panel");
    p.classList.remove("hidden");
    p.innerHTML = `<div><span class="spinner"></span> Computing route…</div>`;
  }
}

function showSingleResult(data, type) {
  const cls   = type === "greedy" ? "greedy-color" : "dp-color";
  const panel = document.getElementById("results-panel");
  panel.classList.remove("hidden");
  panel.innerHTML = `
    <h3 class="${cls}">${data.algorithm}</h3>
    <div class="result-block">
      <div class="result-label">Total Distance</div>
      <div class="result-value ${cls}">${data.total_distance} km</div>
    </div>
    <div class="result-block">
      <div class="result-label">Computation Time</div>
      <div class="result-value">${data.time_ms} ms</div>
    </div>
    <div class="result-block">
      <div class="result-label">Complexity</div>
      <div class="result-value">${data.complexity}</div>
    </div>
    <div class="result-block">
      <div class="result-label">Route Sequence</div>
      <div class="route-sequence">${data.route.join(" → ")}</div>
    </div>
  `;
}

function showCompareResult(data) {
  const g = data.greedy;
  const d = data.dp;
  const imp = data.improvement_percent;
  const dpError = d.error;

  const panel = document.getElementById("results-panel");
  panel.classList.remove("hidden");
  panel.innerHTML = `
    <h3>Comparison</h3>

    <div class="result-block">
      <div class="result-label greedy-color">● Greedy</div>
      <div class="result-value greedy-color">${g.total_distance} km</div>
      <div style="font-size:0.75rem;color:var(--muted);">${g.time_ms} ms &nbsp;|&nbsp; ${g.complexity}</div>
      <div class="route-sequence">${g.route.join(" → ")}</div>
    </div>

    <div class="result-block">
      <div class="result-label dp-color">● DP (Held-Karp)</div>
      ${dpError
        ? `<div class="error-box">${dpError}</div>`
        : `<div class="result-value dp-color">${d.total_distance} km</div>
           <div style="font-size:0.75rem;color:var(--muted);">${d.time_ms} ms &nbsp;|&nbsp; ${d.complexity}</div>
           <div class="route-sequence">${d.route.join(" → ")}</div>`
      }
    </div>

    ${imp !== null && imp !== undefined && !dpError ? `
    <div class="improvement-box">
      <div class="result-label">DP improvement over Greedy</div>
      <div class="result-value accent-color">${imp > 0 ? `${imp}% better` : imp === 0 ? "Same route!" : `Greedy was ${Math.abs(imp)}% better`}</div>
    </div>` : ""}
  `;
}

function showError(msg) {
  const panel = document.getElementById("results-panel");
  panel.classList.remove("hidden");
  panel.innerHTML = `<div class="error-box">⚠ ${msg}</div>`;
}

// ── Init ───────────────────────────────────────────────
loadPreset(6);
