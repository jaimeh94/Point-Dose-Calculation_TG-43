from flask import Flask
from flask import request
from flask import jsonify




# app = Flask('churn')

# @app.route('/predict', methods=['POST'])
# def predict():
#     customer = request.get_json()

#     X = dv.transform([customer])
#     y_pred = model.predict_proba(X)[0,1]
#     churn = y_pred >= 0.5

#     result = {
#         'Question 6 - churn_probability': float(y_pred),
#         'churn': bool(churn)
#     }
#     return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)