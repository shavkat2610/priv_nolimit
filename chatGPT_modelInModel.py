from tensorflow.keras import layers, models

# Define a Sequential submodel
seq_block = models.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
])

# Functional model
inputs = layers.Input(shape=(100,))
x = layers.Dense(128, activation="relu")(inputs)

# Use the Sequential model here
x = seq_block(x)

outputs = layers.Dense(10, activation="softmax")(x)

model = models.Model(inputs, outputs)
model.summary()
