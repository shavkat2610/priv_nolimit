import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Assuming you have a CSV file with 16 features and a binary label (0 or 1)
# For demonstration, we'll generate dummy data
np.random.seed(42)
n_samples = 1000
n_features = 16

# Generate random features
X = np.random.randn(n_samples, n_features)

# Generate binary labels (positive/negative)
y = np.random.randint(0, 2, n_samples)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a model: Random Forest is good for classification with multiple features
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Example prediction on new data
new_data = np.random.randn(1, n_features)  # 1 sample with 16 features
prediction = model.predict(new_data)
print(f"Prediction for new data: {'Positive' if prediction[0] == 1 else 'Negative'}")