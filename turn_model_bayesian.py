import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LayerNormalization, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow import keras
import pickle
import tensorflow as tf
import tensorflow.keras.backend as K

 # custom negative log-likelyhood loss for Gaussian distribution
def gaussian_nll(y_true, y_pred):
    mu = y_pred[:, 0]
    log_sigma = y_pred[:, 1]
    sigma = K.exp(log_sigma)

    return K.mean(
        0.5 * K.log(2 * tf.constant(3.141592653589793))
        + log_sigma
        + 0.5 * K.square((y_true - mu) / sigma)
    )

inputs = ['probability_1_1', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_5', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'equity_flop', 'equity_river', 'decision', 'difference_tocall_n_potheight']
# Load data
df = pd.read_csv('csv_s/turnModel.csv', sep=';')
X = df[inputs].values
y = df['label'].values.astype(float)

# Normalize inputs to [0, 1] (assuming they are in [0, 2] as per your note)
# print(X[0])
# exit()
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

with open(f"turn_model_scaler", "wb") as fp:   #Pickling      
    pickle.dump(scaler, fp) 

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = keras.models.Sequential([
    keras.layers.Input(shape=(len(inputs),)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(2)  # μ and log(σ)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss=gaussian_nll
)

model.summary()




model.fit(
    X_train,
    y_train,        # <-- still ONE value per sample
    validation_data=(X_test, y_test),
    epochs=10000,
    batch_size=20
)

# # Evaluate
# loss, mae = model.evaluate(X_test, y_test, verbose=0)
# print(f"Test Loss (MSE): {loss:.4f}")
# print(f"Test MAE: {mae:.4f}")

# # Predict on new data (example)
# new_data = np.random.rand(1, len(inputs)) * 2  # Random in [0, 2]
# print("New data (before scaling):", new_data)
# new_data_scaled = scaler.transform(new_data)
# print("New data (after scaling):", new_data_scaled)
# prediction = model.predict(new_data_scaled)
# print(f"Predicted value: {prediction[0][0]:.4f}")


model.save('turn_model_bayesian.keras')


