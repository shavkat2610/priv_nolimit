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
learning_rate = 0.000003






# base_model = keras.applications.Xception(
#     weights='imagenet',  # Load weights pre-trained on ImageNet.
#     input_shape=(150, 150, 3),
#     pooling=None,
#     include_top=False)  # Do not include the ImageNet classifier at the top.



# base_model.trainable = False


train_ds = tf.keras.utils.image_dataset_from_directory("datasets/shmol_watgoinon",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
    seed=int(time.time()),
    image_size=(150, 150),
    batch_size=batch_size)

validation_ds = tf.keras.utils.image_dataset_from_directory("datasets/validation_small_shwatsgo",
    label_mode = "categorical",
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
    seed=int(time.time()),
    image_size=(150, 150),
    batch_size=batch_size)


def make_datasets():
    global train_ds, validation_ds
    train_ds = tf.keras.utils.image_dataset_from_directory("datasets/shmol_watgoinon",
        label_mode = "categorical",
        class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
        seed=int(time.time()),
        image_size=(150, 150),
        batch_size=batch_size)

    validation_ds = tf.keras.utils.image_dataset_from_directory("datasets/validation_small_shwatsgo",
        label_mode = "categorical",
        class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"],
        seed=int(time.time()),
        image_size=(150, 150),
        batch_size=batch_size)    


def build_model(dp_rate = 0.72):
    inputs = keras.Input(shape=(150, 150, 3))
    x = keras.layers.Rescaling(1./255, -1)(inputs)
    x = keras.layers.Reshape((150, 150, 3, 1))(x)
    x = keras.layers.Conv3D(16, 3, 1, activation='relu')(x)
    x = keras.layers.Reshape((148, 148, 16, 1))(x)
    x = keras.layers.MaxPool3D()(x)
    x = keras.layers.Conv3D(32, 3, 1, activation='relu')(x)
    x = keras.layers.Reshape((72, 72, 24, 8))(x)
    x = keras.layers.Conv3D(32, 3, (1,1,1), activation='relu')(x)
    x = keras.layers.MaxPooling3D()(x)
    x = keras.layers.Reshape((35, 35, 22, 16))(x)
    x = keras.layers.Conv3D(32, 3, (1,1,1), activation='relu')(x)
    # x3 = keras.layers.Add()([x[:,i,:,0,3] for i in [2,4, 6, 8]])
    # x3 = keras.layers.Flatten()(x3)
    # x3 = keras.layers.Dropout(rate=dp_rate**2.7)(x3)
    # # x3 = keras.layers.Add()([x2, x3])
    # x3 = keras.layers.Dense(17, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x3)
    # x = keras.layers.Reshape((33, 33, 20, 32))(x)
    x = keras.layers.Conv3D(32, 3, 1, activation="relu")(x)
    x = keras.layers.MaxPooling3D()(x)
    # x4 = keras.layers.Add()([x[:,i,:,0,0] for i in [5, 7, 9, 11]])
    # x4 = keras.layers.Flatten()(x4)
    # x4 = keras.layers.Add()([x3, x4])
    # x4 = keras.layers.Dense(64, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x4)
    # x4 = keras.layers.Dropout(rate=dp_rate**2.7)(x4)
    # x = keras.layers.Reshape((15, 15, 9, 32))(x)
    x = keras.layers.Conv3D(32, (3,3,3), (1,1,1),activation='relu')(x)
    x = keras.layers.Reshape((13, 13, 14, 16))(x)
    x = keras.layers.Conv3D(32, (3,3,3), (1,1,1),activation='relu')(x)
    # x = keras.layers.MaxPooling3D()(x)
    # x = keras.layers.Reshape((6, 6, 1, 32))(x)
    x = keras.layers.Conv3D(64, (3,3,3), (1,1,1),activation='relu')(x)
    # x = keras.layers.MaxPooling3D()(x)
    # x = keras.layers.Reshape((1, 1, 2, 64))(x)
    # x = keras.layers.Conv3D(256, (3,3,2), (2,2,1),activation='relu')(x)
    #  = keras.layers.Add()(x[:,:,0,:,:32])
    # x5 = keras.layers.Flatten()(x[:,:,:,0,:64])
    # x5 = keras.layers.Add()([x4, x5])
    # x5 = keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x5)
    # x5 = keras.layers.Dropout(rate=dp_rate)(x5)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(128, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x)
    # x = keras.layers.Concatenate()([x, x5])
    # x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(128, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(64, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x)
    x = keras.layers.LayerNormalization()(x)
    outputs = keras.layers.Dense(6,  kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-4))(x) #(5 values, fifth for nothing, or either of the previous ones checked)
    return keras.Model(inputs, outputs)

model = build_model(0.5)

old_model = keras.saving.load_model("model.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=2, batch_size=batch_size
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_2.keras")







model = build_model(0.7)

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])



make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=5, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_3.keras")






model = build_model(0.73)

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







model = build_model(0.72)

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









model = build_model(0.74)

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









model = build_model()

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














model = build_model()




old_model = keras.saving.load_model("model1_01.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 




model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.95),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# Train end-to-end. Be careful to stop before you overfit!
make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=50, batch_size=batch_size)

model.save("model2_1.keras")



model = build_model()

old_model = keras.saving.load_model("model2_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.85),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model3.keras")




model = build_model()

old_model = keras.saving.load_model("model3.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model4.keras")




model = build_model()

old_model = keras.saving.load_model("model4.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model5.keras")




model = build_model()

old_model = keras.saving.load_model("model5.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model6.keras")




model = build_model()

old_model = keras.saving.load_model("model6.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model7.keras")







model = build_model()

old_model = keras.saving.load_model("model7.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model8.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model9.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.1),
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