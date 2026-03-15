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


def build_model(dp_rate = 0.5):
    inputs = keras.Input(shape=(150, 150, 3))
    x = keras.layers.Rescaling(1./255, -1)(inputs) 
    x = keras.layers.Reshape((150, 150, 3, 1))(x)
    x = keras.layers.Conv3D(2, 3, 3, activation='leaky_relu')(x)
    # x2 = keras.layers.Lambda(lambda x: x[:,:,:,0])(x)
    x2 = keras.layers.Flatten()(x[:,:,:,0 ,0])
    x2 = keras.layers.Dense(1, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x2)
    x = keras.layers.Reshape((50, 50, 2, 1))(x)
    x = keras.layers.Conv3D(4, 2, 2, activation='leaky_relu')(x)
    # x3 = keras.layers.Lambda(lambda x: x[:,:,:,7])(x)
    x3 = keras.layers.Flatten()(x[:,:,:,0 ,3])
    x3 = keras.layers.Dense(2, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x3)
    x = keras.layers.Reshape((25, 25, 4, 1))(x)
    x = keras.layers.Conv3D(8, 2, 2, activation="leaky_relu")(x)
    # x4 = keras.layers.Lambda(lambda x: x[:,:,15], output_shape=x[:, :, 15].shape)(x)
    x4 = keras.layers.Flatten()(x[:,:,:, 1 ,3])
    x4 = keras.layers.Dense(4, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x4)
    x = keras.layers.Reshape((12, 12, 8, 2))(x)
    x = keras.layers.Conv3D(16, 4, 4,activation='relu', kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
    x = keras.layers.MaxPool3D()(x)
    x5 = keras.layers.Flatten()(x[:,:,:, 0,15])
    x5 = keras.layers.Dense(8, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x5)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Concatenate()([x, x2, x3, x4, x5])
    x = keras.layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(32, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
    x = keras.layers.Dropout(rate=dp_rate)(x)
    x = keras.layers.Dense(32, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=2e-5, l2=2e-5),activity_regularizer=keras.regularizers.L2(3e-6))(x)
    x = keras.layers.LayerNormalization()(x)
    outputs = keras.layers.Dense(6)(x) #(5 values, fifth for nothing, or either of the previous ones checked)
    return keras.Model(inputs, outputs)

model = build_model()

# old_model = keras.saving.load_model("model1_3.keras", custom_objects=None, compile=True, safe_mode=True)

# model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00003),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_2.keras")






model = build_model()

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00004),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])



make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_3.keras")





model = build_model()

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00005),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_4.keras")






model = build_model()

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00003),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_5.keras")









model = build_model()

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00003),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_1.keras")
model.save("model1_6.keras")









model = build_model()

old_model = keras.saving.load_model("model1_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.00003),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds,epochs=100, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )
model.save("model1_01.keras")


# base_model.summary()
# exit()














model = build_model()




old_model = keras.saving.load_model("model1_01.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 




model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00005, momentum=0.95),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

# Train end-to-end. Be careful to stop before you overfit!
make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model2_1.keras")



model = build_model()

old_model = keras.saving.load_model("model2_1.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00002, momentum=0.85),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model3.keras")




model = build_model()

old_model = keras.saving.load_model("model3.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00001, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model4.keras")




model = build_model()

old_model = keras.saving.load_model("model4.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00001, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds, validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model5.keras")




model = build_model()

old_model = keras.saving.load_model("model5.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000016, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model6.keras")




model = build_model()

old_model = keras.saving.load_model("model6.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00003, momentum=0.5),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model7.keras")







model = build_model()

old_model = keras.saving.load_model("model7.keras", custom_objects=None, compile=True, safe_mode=True)

model.set_weights(old_model.get_weights()) 

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.0000017, momentum=0.75),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model8.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.00000238, momentum=0.2),
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])

make_datasets()
model.fit(train_ds,validation_data=validation_ds, epochs=100, batch_size=batch_size)

model.save("model9.keras")

model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.000001245678910, momentum=0.1),
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