from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)

FILE_PATH = "anomalies.xlsx"

anomaly_store = {
    "Database": [],
    "OMS": [],
    "Thirdparties": []
}

def read_sheet(sheet_name):
    df = pd.read_excel(FILE_PATH, sheet_name=sheet_name)
    return df.fillna("").to_dict(orient="records")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/anomalies/<system>")
def get_anomalies(system):

    if system not in anomaly_store:
        return jsonify([])

    return jsonify(anomaly_store[system])
    
@app.route("/webhook", methods=["GET"])
def webhook_test():
    return {
        "status": "webhook reachable"
    }

@app.route("/webhook", methods=["POST"])
def webhook():

    print("========== WEBHOOK RECEIVED ==========")

    print("Headers:")
    print(dict(request.headers))

    print("Raw Data:")
    print(request.data)

    print("JSON:")
    print(request.json)

    return {
        "status": "received"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)