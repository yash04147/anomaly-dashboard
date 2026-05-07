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
    

@app.route("/webhook", methods=["POST"])
def webhook():

    payload = request.json

    print("Webhook Payload Received:")
    print(payload)

    # Replace old Thirdparties data completely
    anomaly_store["Thirdparties"] = []

    # If Splunk sends list of results
    if isinstance(payload, list):
        anomaly_store["Thirdparties"] = payload

    # If Splunk sends single object
    else:
        anomaly_store["Thirdparties"].append(payload)

    return {
        "status": "success"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)