import json
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

SHEET_ID = "1SB41Sj9syqUObKsu3S8VKNAdTkm_J2rV0Brk7OiinfU"
SHEET_NAME = "milk_data"  # change if your sheet name is different

def get_month_data(month_name):
    url = f"https://docs.google.com/spreadsheets/d/{1SB41Sj9syqUObKsu3S8VKNAdTkm_J2rV0Brk7OiinfU}/gviz/tq?tqx=out:json&sheet={milk_data}"
    res = requests.get(url)
    text = res.text

    # Extract only the JSON part from the response
    start = text.find("{")
    end = text.rfind("}") + 1
    json_text = text[start:end]

    data = json.loads(json_text)
    rows = data["table"]["rows"]

    for row in rows:
        if not row["c"] or not row["c"][0]:
            continue  # skip empty rows
        month = row["c"][0]["v"]
        if month and month.strip().upper() == month_name.upper():
            return {
                "Month": month,
                "Paid": row["c"][1]["v"] if row["c"][1] else None,
                "Days in Month": row["c"][2]["v"] if row["c"][2] else None,
                "Days Absent": row["c"][3]["v"] if row["c"][3] else None,
                "Days Coming": row["c"][4]["v"] if row["c"][4] else None,
                "Amount": row["c"][5]["v"] if row["c"][5] else None
            }
    return {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/month/<month_name>")
def month_data(month_name):
    data = get_month_data(month_name)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data found for this month"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






