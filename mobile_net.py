import numpy as np
import keras
from keras import layers
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import tensorflow as tf

batch_size = 16






base_model = keras.applications.Xception(
    weights='imagenet',  # Load weights pre-trained on ImageNet.
    input_shape=(150, 150, 3),
    pooling=None,
    include_top=False)  # Do not include the ImageNet classifier at the top.



base_model.trainable = False



train_ds = tf.keras.utils.image_dataset_from_directory("datasets/shmol_watgoinon",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "open_last_card", "run_it_three_times", "buy_in", "connectivity_issues"],
    seed=23,
    image_size=(150, 150),
    batch_size=batch_size)

validation_ds = tf.keras.utils.image_dataset_from_directory("datasets/validation_small_shwatsgo",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "open_last_card", "run_it_three_times", "buy_in", "connectivity_issues"],
    seed=1245103,
    image_size=(150, 150),
    batch_size=batch_size)



inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.17)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.35)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=.45)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.75)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

# old_model = keras.saving.load_model("model.keras", custom_objects=None, compile=True, safe_mode=True)

# model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00003, momentum=0.3),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_2.keras")



inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.2)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.4)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=.375)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00002),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_3.keras")


inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.2)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.6)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00002),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_4.keras")



inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=.45)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.21)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00006),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_5.keras")






inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.7)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.31)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00004),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_6.keras")






inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.Dense(256, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.4)(x)
x = keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.6)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.000003),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_01.keras")


# base_model.summary()
# exit()











inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.1)(x)
x = keras.layers.Dense(256, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.2)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) 
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model1_01.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 


# Freeze all layers except the last few blocks
for layer in base_model.layers:
    if layer.name.startswith('block14'):  # Unfreeze block14 onwards
        layer.trainable = True
    else:
        layer.trainable = False

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000002, momentum=0.95),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# Train end-to-end. Be careful to stop before you overfit!
model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model2_1.keras")

inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.15)(x)
x = keras.layers.Dense(256, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.4)(x)
x = keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model2_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000003, momentum=0.85),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model3.keras")

inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.2)(x)
x = keras.layers.Dense(256, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.4)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.Dropout(rate=.6)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu, kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=1e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model3.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000004, momentum=0.95),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model4.keras")

inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.23)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=0.7)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.8)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu)(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model4.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000008, momentum=0.95),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model5.keras")

inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.3)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=0.7)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.8)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu)(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model5.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000016, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("mode6.keras")

inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=False)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.4)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=0.7)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.8)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu)(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model6.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000032, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model7.keras")


base_model.trainable = True


inputs = keras.Input(shape=(150, 150, 3))
x = keras.layers.Rescaling(1./128, -1)(inputs)
x = base_model(x, training=True)
x = keras.layers.Flatten()(x)
x = keras.layers.Dropout(rate=.45)(x)
x = keras.layers.Dense(256, activation="swish")(x)
x = keras.layers.Dropout(rate=.5)(x)
x = keras.layers.BatchNormalization()(x)
x = keras.layers.Dense(128, activation=keras.activations.leaky_relu)(x)
x = keras.layers.Dropout(rate=0.7)(x)
x = keras.layers.Dense(64, activation="relu")(x)
x = keras.layers.Dropout(rate=.8)(x)
x = keras.layers.Dense(32, activation=keras.activations.leaky_relu)(x)
x = keras.layers.LayerNormalization()(x)
outputs = keras.layers.Dense(9)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
model = keras.Model(inputs, outputs)

old_model = keras.saving.load_model("model7.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.0000017, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model8.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00000238, momentum=0.2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model9.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000001245678910, momentum=0.1),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model20.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model1.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model2.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model3.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model4.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model5.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model6.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model7.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model8.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model9.keras")
print("9")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")

model.fit(train_ds,validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model.keras")



# model.compile(optimizer=keras.optimizers.Adam(),
#               loss=keras.losses.BinaryCrossentropy(from_logits=True),
#               metrics=[keras.metrics.BinaryAccuracy()])
# model.fit(new_dataset, epochs=20, callbacks=..., validation_data=...)