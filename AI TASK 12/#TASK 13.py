#TASK 13
from flask import Flask, request, render_template_string
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# 🔹 Dummy model (yahi pe train ho raha hai, alag file ki zarurat nahi)
X = np.array([[1,2], [2,3], [3,4], [4,5]])
y = np.array([3,5,7,9])

model = LinearRegression()
model.fit(X, y)

# 🔹 HTML bhi yahi embed hai
html = """
<!DOCTYPE html>
<html>
<head>
    <title>ML App</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">

    <h2>ML Prediction App</h2>

    <form action="/predict" method="post">
        <input type="text" name="feature1" placeholder="Feature 1" required><br><br>
        <input type="text" name="feature2" placeholder="Feature 2" required><br><br>

        <button type="submit">Predict</button>
    </form>

    <h3>{{prediction_text}}</h3>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html, prediction_text="")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        f1 = float(request.form['feature1'])
        f2 = float(request.form['feature2'])

        result = model.predict([[f1, f2]])

        return render_template_string(html, prediction_text=f"Result: {result[0]:.2f}")
    except:
        return render_template_string(html, prediction_text="Invalid Input!")

if __name__ == "__main__":
    app.run(debug=True)