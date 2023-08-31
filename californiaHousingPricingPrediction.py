from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

from sklearn.datasets import fetch_california_housing

# Load the california Housing dataset
california = fetch_california_housing()
X = california.data
y = california.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "california_housing_prediction.joblib")
