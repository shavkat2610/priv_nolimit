from keras import layers, models


inputs1 = layers.Input(shape=(100,))
inputs2 = layers.Input(shape=(100,))

shared_block = models.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
])

out1 = shared_block(inputs1)
out2 = shared_block(inputs2)

merged = layers.Concatenate()([out1, out2])
outputs = layers.Dense(1)(merged)

model = models.Model([inputs1, inputs2], outputs)
