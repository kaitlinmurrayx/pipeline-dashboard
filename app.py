"""
StepStone Pipeline Dashboard — Flask Backend
=============================================
Serves the dashboard HTML and provides a /data endpoint.

The /data endpoint is the single source of truth for ALL_DATA and AGG.
Swap out load_pipeline_data() to pull from Salesforce / Snowflake / a DB
instead of the local JSON files.
"""

import json
import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# ---------------------------------------------------------------------------
# Data loader — replace this function to connect to a live data source
# ---------------------------------------------------------------------------

def load_pipeline_data() -> dict:
    """
    Returns a dict with two keys:
      - records : list[dict]  — matches the ALL_DATA schema
      - agg     : dict        — matches the AGG schema (keys: All, SSOF VI, SGPS)

    Current implementation reads from local JSON files in data/.
    To connect to Salesforce/Snowflake, replace this function body with
    your query logic and return the same shape.
    """
    records_path = os.path.join(DATA_DIR, "all_data.json")
    agg_path     = os.path.join(DATA_DIR, "agg.json")

    with open(records_path) as f:
        records = json.load(f)

    with open(agg_path) as f:
        agg = json.load(f)

    return {"records": records, "agg": agg}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the dashboard HTML."""
    return render_template("index.html")


@app.route("/data")
def data():
    """
    Return pipeline data as JSON.

    Response shape:
    {
      "records": [ { "fund": ..., "account": ..., ... }, ... ],
      "agg":     { "All": {...}, "SSOF VI": {...}, "SGPS": {...} }
    }
    """
    payload = load_pipeline_data()
    response = jsonify(payload)
    # Allow the browser to cache for 5 minutes; remove if you want always-fresh data
    response.cache_control.max_age = 300
    return response


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True gives live reload; set to False for production
    app.run(debug=True, port=5000)
