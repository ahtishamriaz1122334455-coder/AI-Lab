# ============================================================
#   LOAN APPROVAL AI SYSTEM
#   Run karna:  python loan_ai.py
# ============================================================

# Step 1: Libraries install karo (agar pehli baar hai)
import subprocess, sys

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

print("Libraries check ho rahi hain...")
for pkg in ["flask", "pandas", "scikit-learn", "numpy"]:
    try:
        __import__(pkg if pkg != "scikit-learn" else "sklearn")
    except ImportError:
        print(f"  Installing {pkg}...")
        install(pkg)

print("Sab libraries ready!\n")

# ============================================================
# Step 2: Imports
# ============================================================
import os, threading, webbrowser
import pandas as pd
import numpy as np
from flask import Flask, render_template_string, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# ============================================================
# Step 3: Dataset dhundho
# ============================================================
def find_dataset():
    possible = [
        "Training Dataset.csv",
        "training dataset.csv",
        "train.csv",
        "loan.csv",
        "dataset.csv",
    ]
    # Current folder check
    for name in possible:
        if os.path.exists(name):
            return name
    # Downloads folder check
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    for name in possible:
        path = os.path.join(downloads, name)
        if os.path.exists(path):
            return path
    return None

# ============================================================
# Step 4: Model train karo
# ============================================================
trained_model     = None
model_accuracies  = {}
feature_columns   = None
encoders          = {}

def train():
    global trained_model, model_accuracies, feature_columns, encoders

    csv_path = find_dataset()
    if not csv_path:
        print("\n" + "="*50)
        print("  ERROR: Dataset CSV file nahi mili!")
        print("  'Training Dataset.csv' is folder mein rakhein:")
        print(f"  {os.getcwd()}")
        print("="*50 + "\n")
        return False

    print(f"Dataset mili: {csv_path}")
    data = pd.read_csv(csv_path)

    # Clean
    data = data.drop("Loan_ID", axis=1, errors="ignore")
    for col in data.columns:
        if data[col].dtype in ["int64", "float64"]:
            data[col] = data[col].fillna(data[col].median())
        else:
            data[col] = data[col].fillna(data[col].mode()[0])

    # Encode
    encoders = {}
    cat_cols = data.select_dtypes(include="object").columns.tolist()
    if "Loan_Status" in cat_cols:
        cat_cols.remove("Loan_Status")
    for col in cat_cols:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        encoders[col] = le

    data["Loan_Status"] = data["Loan_Status"].map({"Y": 1, "N": 0})

    target = [c for c in data.columns if "Loan_Status" in c][0]
    X = data.drop(target, axis=1)
    y = data[target]
    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree":       DecisionTreeClassifier(),
        "Random Forest":       RandomForestClassifier(),
    }

    best_score = 0
    best_model = None
    for name, m in models.items():
        m.fit(X_train, y_train)
        acc = round(accuracy_score(y_test, m.predict(X_test)) * 100, 1)
        model_accuracies[name] = acc
        print(f"  {name}: {acc}%")
        if acc > best_score:
            best_score = acc
            best_model = m

    trained_model = best_model
    print(f"\nBest model ready! Accuracy: {best_score}%")
    return True

# ============================================================
# Step 5: HTML page (poora frontend)
# ============================================================
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Loan Approval AI</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; padding: 2rem 1rem; }
    .app { max-width: 720px; margin: 0 auto; }

    .header { text-align: center; margin-bottom: 2rem; }
    .badge { display: inline-block; background: #dbeafe; color: #1d4ed8; font-size: 12px; padding: 4px 14px; border-radius: 20px; margin-bottom: 10px; }
    .header h1 { font-size: 26px; font-weight: 700; margin-bottom: 6px; }
    .header p  { font-size: 14px; color: #6b7280; }

    .stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.5rem; }
    .stat  { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; text-align: center; }
    .stat-val   { font-size: 20px; font-weight: 700; color: #1d4ed8; }
    .stat-label { font-size: 11px; color: #9ca3af; margin-top: 3px; }

    .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.4rem 1.5rem; margin-bottom: 1rem; }
    .sec  { font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: .07em; margin-bottom: 1rem; }

    .g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
    .g3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }

    .field { display: flex; flex-direction: column; gap: 5px; }
    .field label  { font-size: 13px; color: #374151; font-weight: 500; }
    .field input, .field select {
      font-size: 14px; padding: 9px 11px;
      border: 1px solid #d1d5db; border-radius: 8px;
      background: #f9fafb; color: #111; width: 100%;
      transition: border-color .2s;
    }
    .field input:focus, .field select:focus {
      outline: none; border-color: #3b82f6; background: #fff;
    }

    .btn {
      width: 100%; padding: 14px; font-size: 16px; font-weight: 600;
      border: none; border-radius: 10px; background: #1d4ed8; color: #fff;
      cursor: pointer; margin-top: .5rem; transition: background .2s;
    }
    .btn:hover    { background: #1e40af; }
    .btn:disabled { opacity: .5; cursor: not-allowed; }

    .loading { display:none; text-align:center; padding:1.2rem; color:#6b7280; font-size:14px; }
    .spin {
      display: inline-block; width:18px; height:18px;
      border: 2px solid #e5e7eb; border-top-color: #3b82f6;
      border-radius: 50%; animation: spin .7s linear infinite;
      vertical-align: middle; margin-right: 8px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .result { display:none; border-radius:12px; padding:1.8rem; text-align:center; margin-top:1rem; border:1px solid #e5e7eb; }
    .result.ok  { background:#f0fdf4; border-color:#86efac; }
    .result.bad { background:#fff1f2; border-color:#fda4af; }
    .r-icon  { font-size:48px; margin-bottom:8px; }
    .r-title { font-size:24px; font-weight:700; margin-bottom:8px; }
    .ok  .r-title { color:#16a34a; }
    .bad .r-title { color:#dc2626; }
    .r-text { font-size:14px; color:#4b5563; margin-bottom:14px; line-height:1.6; }

    .bars { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .bar-box { background:#f9fafb; border:1px solid #e5e7eb; border-radius:8px; padding:12px; }
    .bar-lbl  { font-size:12px; color:#6b7280; margin-bottom:6px; }
    .bar-bg   { height:8px; border-radius:4px; background:#e5e7eb; overflow:hidden; }
    .bar-fill { height:100%; border-radius:4px; transition:width .6s ease; }
    .g-fill   { background:#16a34a; }
    .r-fill   { background:#dc2626; }
    .bar-num  { font-size:16px; font-weight:700; margin-top:4px; }
    .g-num { color:#16a34a; }
    .r-num { color:#dc2626; }

    @media(max-width:560px){ .g2,.g3,.stats,.bars{ grid-template-columns:1fr; } }
  </style>
</head>
<body>
<div class="app">

  <div class="header">
    <div class="badge">Real ML Model • Trained on your data</div>
    <h1>Loan Approval AI System</h1>
    <p>Form bharein aur ML model se prediction len</p>
  </div>

  <div class="stats" id="stats-bar"></div>

  <div class="card">
    <div class="sec">Personal information</div>
    <div class="g2">
      <div class="field"><label>Gender</label>
        <select id="gender"><option value="Male">Male</option><option value="Female">Female</option></select>
      </div>
      <div class="field"><label>Marital Status</label>
        <select id="married"><option value="Yes">Married</option><option value="No">Unmarried</option></select>
      </div>
    </div>
    <div class="g3">
      <div class="field"><label>Dependents</label>
        <select id="dependents"><option>0</option><option>1</option><option>2</option><option value="3+">3+</option></select>
      </div>
      <div class="field"><label>Education</label>
        <select id="education"><option value="Graduate">Graduate</option><option value="Not Graduate">Not Graduate</option></select>
      </div>
      <div class="field"><label>Self Employed</label>
        <select id="self_employed"><option value="No">No</option><option value="Yes">Yes</option></select>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="sec">Financial details</div>
    <div class="g2">
      <div class="field"><label>Applicant Income</label>
        <input type="number" id="applicant_income" value="50000" min="0"/>
      </div>
      <div class="field"><label>Co-applicant Income</label>
        <input type="number" id="coapplicant_income" value="0" min="0"/>
      </div>
    </div>
    <div class="g3">
      <div class="field"><label>Loan Amount (thousands)</label>
        <input type="number" id="loan_amount" value="150" min="0"/>
      </div>
      <div class="field"><label>Loan Term (months)</label>
        <select id="loan_term">
          <option value="360">360</option><option value="180">180</option>
          <option value="120">120</option><option value="84">84</option>
          <option value="60">60</option><option value="36">36</option><option value="12">12</option>
        </select>
      </div>
      <div class="field"><label>Credit History</label>
        <select id="credit_history"><option value="1">Clear (1)</option><option value="0">Issues (0)</option></select>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="sec">Property details</div>
    <div class="field"><label>Property Area</label>
      <select id="property_area">
        <option value="Urban">Urban</option>
        <option value="Semiurban">Semiurban</option>
        <option value="Rural">Rural</option>
      </select>
    </div>
  </div>

  <button class="btn" onclick="predict()">Predict Loan Approval</button>

  <div class="loading" id="loading">
    <span class="spin"></span> Model calculate kar raha hai...
  </div>

  <div class="result" id="result">
    <div class="r-icon"  id="r-icon"></div>
    <div class="r-title" id="r-title"></div>
    <div class="r-text"  id="r-text"></div>
    <div class="bars">
      <div class="bar-box">
        <div class="bar-lbl">Approval probability</div>
        <div class="bar-bg"><div class="bar-fill g-fill" id="b-ok" style="width:0%"></div></div>
        <div class="bar-num g-num" id="v-ok">0%</div>
      </div>
      <div class="bar-box">
        <div class="bar-lbl">Rejection probability</div>
        <div class="bar-bg"><div class="bar-fill r-fill" id="b-no" style="width:0%"></div></div>
        <div class="bar-num r-num" id="v-no">0%</div>
      </div>
    </div>
  </div>

</div>
<script>
  // Model accuracy stats load karo
  fetch('/stats').then(r=>r.json()).then(data=>{
    const bar = document.getElementById('stats-bar');
    bar.innerHTML = Object.entries(data).map(([name,acc])=>
      `<div class="stat"><div class="stat-val">${acc}%</div><div class="stat-label">${name}</div></div>`
    ).join('');
  });

  async function predict() {
    const btn = document.querySelector('.btn');
    const loading = document.getElementById('loading');
    const result  = document.getElementById('result');
    btn.disabled = true;
    loading.style.display = 'block';
    result.style.display  = 'none';

    const payload = {
      gender:             document.getElementById('gender').value,
      married:            document.getElementById('married').value,
      dependents:         document.getElementById('dependents').value,
      education:          document.getElementById('education').value,
      self_employed:      document.getElementById('self_employed').value,
      applicant_income:   document.getElementById('applicant_income').value,
      coapplicant_income: document.getElementById('coapplicant_income').value,
      loan_amount:        document.getElementById('loan_amount').value,
      loan_term:          document.getElementById('loan_term').value,
      credit_history:     document.getElementById('credit_history').value,
      property_area:      document.getElementById('property_area').value,
    };

    const res  = await fetch('/predict', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    const data = await res.json();

    loading.style.display = 'none';
    btn.disabled = false;

    const ok = data.decision === 'APPROVED';
    result.className = 'result ' + (ok ? 'ok' : 'bad');
    result.style.display = 'block';
    document.getElementById('r-icon').textContent  = ok ? '✅' : '❌';
    document.getElementById('r-title').textContent = ok ? 'Loan Approved!' : 'Loan Rejected';
    document.getElementById('r-text').textContent  = `Model confidence: ${data.confidence}%`;
    document.getElementById('b-ok').style.width = data.approved_prob + '%';
    document.getElementById('v-ok').textContent = data.approved_prob + '%';
    document.getElementById('b-no').style.width = data.rejected_prob + '%';
    document.getElementById('v-no').textContent = data.rejected_prob + '%';
    result.scrollIntoView({behavior:'smooth', block:'nearest'});
  }
</script>
</body>
</html>
"""

# ============================================================
# Step 6: Flask routes
# ============================================================
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/stats')
def stats():
    return jsonify(model_accuracies)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        d = request.json
        row = []
        for col in feature_columns:
            mapping = {
                'Gender': d.get('gender','Male'),
                'Married': d.get('married','Yes'),
                'Dependents': d.get('dependents','0'),
                'Education': d.get('education','Graduate'),
                'Self_Employed': d.get('self_employed','No'),
                'ApplicantIncome': float(d.get('applicant_income',0)),
                'CoapplicantIncome': float(d.get('coapplicant_income',0)),
                'LoanAmount': float(d.get('loan_amount',0)),
                'Loan_Amount_Term': float(d.get('loan_term',360)),
                'Credit_History': float(d.get('credit_history',1)),
                'Property_Area': d.get('property_area','Urban'),
            }
            val = mapping.get(col, 0)
            if col in encoders:
                try:
                    val = encoders[col].transform([str(val)])[0]
                except:
                    val = 0
            row.append(val)

        pred  = trained_model.predict([row])[0]
        proba = trained_model.predict_proba([row])[0]
        return jsonify({
            "decision":      "APPROVED" if pred == 1 else "REJECTED",
            "confidence":    round(max(proba)*100, 1),
            "approved_prob": round(proba[1]*100, 1),
            "rejected_prob": round(proba[0]*100, 1),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Step 7: Run!
# ============================================================
if __name__ == '__main__':
    print("=" * 50)
    print("   LOAN APPROVAL AI SYSTEM")
    print("=" * 50)
    print("\nModels train ho rahe hain...")

    ok = train()
    if not ok:
        input("\nEnter dabao band karne ke liye...")
        sys.exit()

    print("\nBrowser mein khul raha hai...")
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    print("\n" + "="*50)
    print("  Server chal raha hai: http://127.0.0.1:5000")
    print("  Band karne ke liye: Ctrl + C")
    print("="*50 + "\n")
    app.run(debug=False)