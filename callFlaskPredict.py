import requests

# Prepare the data payload
payload = {
    "MedInc": 3.2596,
    "HouseAge": 33,
    "AveRooms": 5.017657,
    "AveBedrms": 1.006421,
    "Population": 2300,
    "AveOccup": 3.691814,
    "Latitude": 32.71,
    "Longitude": -117.03
}

# Make the POST request
response = requests.post(
    "http://127.0.0.1:5000/predict",
    headers={"Content-Type": "application/json"},
    json=payload
)

# Parse and print the response
if response.status_code == 200:
    print("Predicted value:", response.json()['prediction'])
else:
    print("Failed to get a prediction. Status code:", response.status_code)
