from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

def parse_cams_statement(file):
    df = pd.read_csv(file)
    # Simplified CSV parser—expand as needed
    return df

def evaluate_mutual_funds(mf_data):
    return [{"current_fund": row["Fund"], "suggested_switch": "Mirae Asset Large Cap", "reason": "Better 5Y return/expense ratio"} for _, row in mf_data.iterrows()]

def compute_tax_saving(recurring):
    used = recurring.get("EPF", 0)*12 + recurring.get("NPS", 0)*12
    limit = 150000
    return {"80C_used": used, "80C_limit": limit, "extra_suggestion": f"Invest additional ₹{max(0, limit - used)} in ELSS"}

def compute_return_projection(mf_data):
    return {"expected_annual_return": "11.2%", "suggested_allocation": {"Equity": 60, "Debt": 30, "Liquid": 10}}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    mf_data = parse_cams_statement(file)
    return jsonify({"parsed_data": mf_data.to_dict(orient="records")})

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    mf_df = pd.DataFrame(data['mutual_funds'])
    recurring = data.get('recurring_investments', {})
    liquid_cash = data.get('liquid_cash', 0)
    mf_suggestions = evaluate_mutual_funds(mf_df)
    tax_strategy = compute_tax_saving(recurring)
    returns_projection = compute_return_projection(mf_df)
    return jsonify({
        "mf_switch_suggestions": mf_suggestions,
        "tax_saving_strategy": tax_strategy,
        "returns_projection": returns_projection
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
