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

batch_size = 128
learning_rate = 0.000015 # 0.000005






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
    print("building model with dropout rate: "+str(dp_rate))
    inputs = keras.Input(shape=(375, 375, 3))
    x = keras.layers.Rescaling(1./255, -1)(inputs)
    x = keras.layers.Reshape((375, 375, 3, 1))(x)
    x = keras.layers.Conv3D(16, 3, (2,2,1), activation='swish')(x)
    x = keras.layers.Reshape((187, 187, 16, 1))(x)

    x0 = keras.layers.Conv3D(16, (3,3,2), (5,5,16), activation='swish')(x)
    x0 = keras.layers.MaxPooling3D((7,7,1))(x0)
    x0 = keras.layers.Conv3D(16, (5, 5, 1), (1,1,1), activation='swish')(x0)
    x0 = keras.layers.Flatten()(x0)

    x = keras.layers.MaxPooling3D((2,2,1))(x)
    x = keras.layers.Conv3D(16, (3, 3, 3), (2,2,2), activation='swish')(x)

    x1 = keras.layers.Conv3D(16, (3, 3, 2), (4,4,3), activation='linear')(x)
    x1 = keras.layers.MaxPooling3D((3, 3, 2))(x1)
    x1 = keras.layers.Conv3D(16, (3, 3, 1), (1,1,1), activation='linear')(x1)
    x1 = keras.layers.Flatten()(x1)

    x = keras.layers.Conv3D(16, (3, 3, 3), (2,2,2), activation='swish')(x)

    x2 = keras.layers.Conv3D(16, (3, 3, 2), (4,4,2), activation='linear')(x)
    x2 = keras.layers.Conv3D(16, (5, 5, 1), (1,1,1), activation='swish')(x2)
    x2 = keras.layers.Flatten()(x2)

    x = keras.layers.Conv3D(16, (3, 3, 2), (2,2,1), activation='swish')(x)
    
    x3 = keras.layers.Flatten()(x[:,:,3,1,3])

    x = keras.layers.Conv3D(64, (5, 5, 2), (5,5,1), activation="linear")(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(256, activation="leaky_relu")(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Concatenate()([x, x0, x1])
    x = keras.layers.Dense(256, activation="leaky_relu")(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Concatenate()([x, x2, x3])
    x = keras.layers.Dense(256, activation="leaky_relu")(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(64, activation="leaky_relu")(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(16, activation="leaky_relu")(x)
    # x = keras.layers.LayerNormalization()(x)
    outputs = keras.layers.Dense(6)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
    return keras.Model(inputs, outputs)

model = build_model(0.0)

old_model = keras.saving.load_model("model.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights())

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate/2.0),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=2, batch_size=batch_size
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_2.keras")







model = build_model(0.125)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*2.0),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])



make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=2, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_3.keras")






model = build_model(0.25)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=10, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_4.keras")







model = build_model(0.35)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=20, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_5.keras")









model = build_model(0.45)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*3),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=30, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_6.keras")









model = build_model(.5)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=40, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_01.keras")


# base_model.summary()
# exit()














model = build_model(.5)




old_model = keras.saving.load_model("model1_01.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 




model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate*2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# Train end-to-end. Be careful to stop before you overfit!
make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model2_1.keras")



model = build_model(.5)

old_model = keras.saving.load_model("model2_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model3.keras")




model = build_model(.5)

old_model = keras.saving.load_model("model3.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model4.keras")




model = build_model(.54)

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

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
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

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model8.keras")

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model9.keras")

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
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