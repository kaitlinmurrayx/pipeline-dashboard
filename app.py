import os
from flask import Flask, render_template, Response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ALL_DATA_FILE = os.path.join(DATA_DIR, "all_data.json")
AGG_FILE = os.path.join(DATA_DIR, "agg.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    try:
        with open(ALL_DATA_FILE, "r", encoding="utf-8") as f:
            all_data_json = f.read()

        with open(AGG_FILE, "r", encoding="utf-8") as f:
            agg_json = f.read()

        payload = f'{{"records":{all_data_json},"agg":{agg_json}}}'
        return Response(payload, mimetype="application/json")

    except Exception as e:
        print("ERROR LOADING DATA:", str(e))
        return Response('{"error":"Data load failed"}', mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
``
