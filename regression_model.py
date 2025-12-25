import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

# Load your data
df = pd.read_csv('csv_s/turnModel.csv', sep=';')
X = df[['probability_1_1', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_5', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'hand_score', 'pro_1_1_river']].values
y = df['label'].values.astype(float)  # Ensure y is float for regression

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose and train model (Random Forest Regressor)
model = RandomForestRegressor(n_estimators=100000, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# # Example prediction on new data
# new_data = np.random.randn(1, 16)  # Replace with your 16 inputs
# prediction = model.predict(new_data)
# print(f"Predicted value: {prediction[0]:.4f}")