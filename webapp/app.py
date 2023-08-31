from flask import Flask, request, jsonify

import json
import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np

app = Flask(__name__)

def scale(payload):
    scaler = StandardScaler().fit(payload)
    return scaler.transform(payload)

@app.route("/")
def home():
    return "<h3>Sklearn Prediction Container</h3>"

@app.route("/predict", methods=['POST'])
def predict():
    """
        Input sample:
    		{
    		  "MedInc": 3.2596,
    		  "HouseAge": 33,
    		  "AveRooms": 5.017657,
    		  "AveBedrms": 1.006421,
    		  "Population": 2300,
    		  "AveOccup": 3.691814,
    		  "Latitude": 32.71,
    		  "Longitude": -117.03
    		}

        Output sample:
            {"prediction" : [1.9372587405453814]}
    """
    try:
        loaded_model = joblib.load("california_housing_prediction.joblib")

        # Since you're expecting JSON, you can use request.json directly
        data_dict = request.json

        values_list = list(data_dict.values())
        sample_data_point = np.array([values_list])

        predicted_value = loaded_model.predict(sample_data_point)

        # Convert the NumPy array to a Python list
        return jsonify({'prediction': predicted_value.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/metadata", methods=["GET"])
def metadata():
    try:
        # Load the trained model from the file
        loaded_model = joblib.load("california_housing_prediction.joblib")
    except Exception as e:
        return jsonify({"error": str(e)})

    # Extract model metadata
    coef = loaded_model.coef_
    intercept = loaded_model.intercept_

    feature_names = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']

    feature_coef_map = {}
    for feature, coef_value in zip(feature_names, coef):
        feature_coef_map[feature] = coef_value

    return jsonify({
        "model_coefficients": feature_coef_map,
        "model_intercept": intercept,
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
