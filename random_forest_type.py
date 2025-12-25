

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import csv

# Load your data (replace with your CSV path)
df = pd.read_csv('csv_s/turnModel.csv', sep=';')
X = df['probability_1_1', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_5', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'hand_score', 'pro_1_1_river'].values
y = df['label'].values

# # For demonstration, generate dummy data
# np.random.seed(42)
# n_samples = 1000
# n_features = 16
# x = []
# y = []

# # Open the CSV file in read mode
# with open('csv_s/turnModel.csv', 'r') as csvfile:
#   # Create a reader object
#   csv_reader = csv.reader(csvfile, delimiter=";")
#   next(csv_reader)
#   # Iterate through the rows in the CSV file
#   for row in csv_reader:
#     x.append(row[:-1])
#     y.append(row[-1])

#     # Access each element in the row

# x2 = []
# for input_ in x:
#    x2.append(np.array(list(map(float, input_))))

# X = np.array(x2)
# y = np.array(list(map(float, y)))

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

# Choose and train model
model = RandomForestClassifier(n_estimators=100, random_state=22)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Predict on new data
new_data = np.random.randn(1, 16)  # Replace with your 16 inputs
prediction = model.predict(new_data)
print(f"Prediction: {'Positive' if prediction[0] >= 0 else 'Negative'}")

