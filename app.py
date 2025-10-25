import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

SHEET_ID = "1SB41Sj9syqUObKsu3S8VKNAdTkm_J2rV0Brk7OiinfU"  # Replace this with your real sheet ID
SHEET_NAME = "milk_data"  # Or whatever your sheet is named

def get_month_data(month_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:json&sheet={SHEET_NAME}"
    res = requests.get(url)
    text = res.text
    json_text = text[text.find("{"):text.rfind("}")+1]  # clean response
    import json
    data = json.loads(json_text)

    rows = data["table"]["rows"]
    for row in rows:
        month = row["c"][0]["v"]
        if month and month.strip().upper() == month_name.upper():
            return {
                "Month": month,
                "Paid": row["c"][1]["v"],
                "Days in Month": row["c"][2]["v"],
                "Days Absent": row["c"][3]["v"],
                "Days Coming": row["c"][4]["v"],
                "Amount": row["c"][5]["v"]
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



