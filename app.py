"""
Bus Routing & Student Drop-off System
Flask Backend
"""
from flask import Flask, render_template, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from algorithms.routing import greedy_route, dp_route, compare

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/greedy", methods=["POST"])
def api_greedy():
    data = request.get_json()
    stops = data.get("stops", [])
    depot = data.get("depot", 0)
    if len(stops) < 2:
        return jsonify({"error": "Need at least 2 stops"}), 400
    result = greedy_route(stops, depot)
    return jsonify(result)


@app.route("/api/dp", methods=["POST"])
def api_dp():
    data = request.get_json()
    stops = data.get("stops", [])
    depot = data.get("depot", 0)
    if len(stops) < 2:
        return jsonify({"error": "Need at least 2 stops"}), 400
    result = dp_route(stops, depot)
    return jsonify(result)


@app.route("/api/compare", methods=["POST"])
def api_compare():
    data = request.get_json()
    stops = data.get("stops", [])
    depot = data.get("depot", 0)
    if len(stops) < 2:
        return jsonify({"error": "Need at least 2 stops"}), 400
    result = compare(stops, depot)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
