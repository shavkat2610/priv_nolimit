
from keras import layers, models

conv_block = models.Sequential([
    layers.Conv2D(32, 3, padding="same", activation="relu"),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
])

inputs = layers.Input(shape=(64, 64, 3))
x = conv_block(inputs)
x = conv_block(x)   # reused block
outputs = layers.Flatten()(x)

model = models.Model(inputs, outputs)
