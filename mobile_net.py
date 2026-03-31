from keras.applications import MobileNetV2
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.layers import Input
import numpy as np
import keras
from keras import layers
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import tensorflow as tf
import time

batch_size = 64
learning_rate = 0.0001 # 0.000005






# base_model = keras.applications.Xception(
#     weights='imagenet',  # Load weights pre-trained on ImageNet.
#     input_shape=(375, 375, 3),
#     pooling=None,
#     include_top=False)  # Do not include the ImageNet classifier at the top.



# base_model.trainable = False


train_ds = tf.keras.utils.image_dataset_from_directory("datasets/shmol_watgoinon",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
    seed=int(time.time()),
    image_size=(375, 375),
    batch_size=batch_size, 
    interpolation="nearest"
)

validation_ds = tf.keras.utils.image_dataset_from_directory("datasets/validation_small_shwatsgo",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
    seed=int(time.time()),
    image_size=(375, 375),
    batch_size=batch_size, 
    interpolation="nearest"
)


def make_datasets():
    global train_ds, validation_ds
    train_ds = tf.keras.utils.image_dataset_from_directory("datasets/shmol_watgoinon",
        label_mode = "categorical",
        class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
        seed=int(time.time()),
        image_size=(375, 375),
        batch_size=batch_size, 
        interpolation="nearest"
    )

    validation_ds = tf.keras.utils.image_dataset_from_directory("datasets/validation_small_shwatsgo",
        label_mode = "categorical",
        class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
        seed=int(time.time()),
        image_size=(375, 375),
        batch_size=batch_size, 
        interpolation="nearest"
    )    


def build_model(dp_rate = 0.65):
    input_tensor = keras.Input(shape=(375, 375, 3))
    # x = keras.layers.Rescaling(1./255, -1)(input_tensor)
    base_model = MobileNetV2(input_tensor=input_tensor, weights='imagenet', include_top=True)    
    x = base_model.output
    x = keras.layers.Flatten()(x)
    # x = keras.layers.Dense(256, activation="leaky_relu")(x)
    # x = keras.layers.Dropout(rate=dp_rate)(x)
    # x = keras.layers.Dense(256, activation="leaky_relu")(x)
    outputs = keras.layers.Dense(6)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
    model = keras.Model(base_model.input, outputs)
    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    for layer in base_model.layers:
        layer.trainable = False
    # compile the model (should be done *after* setting layers to non-trainable)
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy')    
    return model, base_model

model, _ = build_model(0.25)

# old_model = keras.saving.load_model("model.keras", custom_objects=None, compile=True, safe_mode=True)

# model.set_weights(old_model.get_weights())

model.summary()


# make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=20, batch_size=batch_size
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_2.keras")







model, base_model = build_model(0.5)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 



# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

print("\n at this point, the top layers are well trained and we can start fine-tuning \n convolutional layers from inception V3. We will freeze the bottom N layers \n and train the remaining top layers.")

# let's visualize layer names and layer indices to see how many layers
print("\n# let's visualize layer names and layer indices to see how many layers\n")
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
print("\n# we chose to train the top 2 inception blocks, i.e. we will freeze \n")
# the first 249 layers and unfreeze the rest:
for layer in base_model.layers[:249]:
   layer.trainable = False
for layer in base_model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

model.summary()

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=25, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_3.keras")



exit()


model = build_model(0.15)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=15, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_4.keras")







model = build_model(0.17)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=30, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_5.keras")









model = build_model(0.15)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=40, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_6.keras")









model = build_model(.2)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_01.keras")


# base_model.summary()
# exit()














model = build_model(.25)




old_model = keras.saving.load_model("model1_01.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 




model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# Train end-to-end. Be careful to stop before you overfit!
make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model2_1.keras")



model = build_model(.3)

old_model = keras.saving.load_model("model2_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate, momentum=0.85),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model3.keras")




model = build_model(.35)

old_model = keras.saving.load_model("model3.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model4.keras")




model = build_model(.4)

old_model = keras.saving.load_model("model4.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model5.keras")




model = build_model(.45)

old_model = keras.saving.load_model("model5.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model6.keras")




model = build_model(.5)

old_model = keras.saving.load_model("model6.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model7.keras")







model = build_model(.6)

old_model = keras.saving.load_model("model7.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model8.keras")

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate, momentum=0.2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model9.keras")

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate, momentum=0.1),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model20.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model1.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model2.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model3.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model4.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model5.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model6.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model7.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model8.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model9.keras")
print("9")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model.keras")



# model.compile(optimizer=keras.optimizers.Adam(),
#               loss=keras.losses.BinaryCrossentropy(from_logits=True),
#               metrics=[keras.metrics.BinaryAccuracy()])
# make_datasets()
# model.fit(train_ds, epochs=20, callbacks=..., validation_data=validation_ds)