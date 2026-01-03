import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LayerNormalization, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow import keras
import pickle




inputs = ['probability_1_1', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_4', 'average_pot_5', 'average_pot_6', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'equity_flop', 'equity_river', 'decision', 'difference_tocall_n_potheight']
# Load data
df = pd.read_csv('csv_s/turnModel.csv', sep=';')
X = df[inputs].values
y = df['label'].values.astype(float)


with open("turn_model_scaler", "rb") as fp:   # Unpickling
    scaler = pickle.load(fp)  

# Normalize inputs to [0, 1] (assuming they are in [0, 2] as per your note)
# scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.transform(X)

with open(f"turn_model_scaler", "wb") as fp:   #Pickling      
    pickle.dump(scaler, fp) 


# Build model
model = Sequential([
    Dense(512, input_dim=len(inputs), activation='leaky_relu'),
    # Dropout(0.95),
    Dense(256, activation='swish', kernel_regularizer=keras.regularizers.L1L2(l1=1e-4, l2=1e-5),activity_regularizer=keras.regularizers.L2(1e-4)),
    # Dropout(0.95),
    Dense(128, activation='swish', kernel_regularizer=keras.regularizers.L1L2(l1=1e-4, l2=1e-5),activity_regularizer=keras.regularizers.L2(1e-4)),
    # Dropout(0.95),
    Dense(64, activation='relu', kernel_regularizer=keras.regularizers.L1L2(l1=1e-4, l2=1e-5),activity_regularizer=keras.regularizers.L2(1e-4)),
    Dense(32, activation='swish', kernel_regularizer=keras.regularizers.L1L2(l1=1e-4, l2=1e-5),activity_regularizer=keras.regularizers.L2(1e-4)),
    LayerNormalization(),
    Dense(16, activation='selu'),
    Dense(8, activation='relu'),
    # Dropout(0.75),
    Dense(4, activation='relu'),
    Dense(2, activation='relu'),
    Dense(1, activation='linear')  # Linear for regression output in [-1, 2]
])

# Compile
model.compile(optimizer=SGD(learning_rate=0.000001, momentum=0.99), loss='mse', metrics=['mae'])

# Train
history = model.fit(X, y, epochs=10000, batch_size=8, validation_split=0.2, verbose=1)

# # Evaluate
# loss, mae = model.evaluate(X_test, y_test, verbose=0)
# print(f"Test Loss (MSE): {loss:.4f}")
# print(f"Test MAE: {mae:.4f}")

# # Predict on new data (example)
# new_data = np.random.rand(1, len(inputs)) * 2  # Random in [0, 2]
# new_data_scaled = scaler.transform(new_data)
# prediction = model.predict(new_data_scaled)
# print(f"Predicted value: {prediction[0][0]:.4f}")


model.save('turn_model.keras')


