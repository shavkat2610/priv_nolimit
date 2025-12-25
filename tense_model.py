import keras
import csv
import numpy as np




batch_size = 4










def build_model(num_inputs = 20):

    inputs = keras.Input(shape=(num_inputs,))
    x1 = keras.layers.Dense(12)(inputs)
    x2 = keras.layers.Dense(12)(inputs)
    x3 = keras.layers.Dense(12)(inputs)
    x4 = keras.layers.Dense(12)(inputs)
    x5 = keras.layers.Dense(12)(inputs)
    x6 = keras.layers.Dense(12)(inputs)
    x7 = keras.layers.Dense(12)(inputs)
    x8 = keras.layers.Dense(12)(inputs)
    x9 = keras.layers.Dense(12)(inputs) # residual

    x1 = keras.layers.BatchNormalization()(x1)
    x2 = keras.layers.LayerNormalization()(x2)
    x3 = keras.layers.BatchNormalization()(x3)
    x5 = keras.layers.BatchNormalization()(x5)
    x7 = keras.layers.BatchNormalization()(x7)
    x10 = keras.layers.LayerNormalization()(x9)
    x11 = keras.layers.BatchNormalization()(x9)
    x12 = keras.layers.LayerNormalization()(x9)
    

    x9 = keras.layers.BatchNormalization()(x9)
    x9 = keras.layers.Dense(18, activation="elu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x9)
    x4 = keras.layers.LayerNormalization()(x4)
    x6 = keras.layers.LayerNormalization()(x6)
    x8 = keras.layers.LayerNormalization()(x8)
    x1_c = keras.layers.Concatenate()([x1, x2])
    x2_c = keras.layers.Concatenate()([x3, x10])
    x3_c = keras.layers.Concatenate()([x5, x11])
    x4_c = keras.layers.Concatenate()([x7, x12])

    x1 = keras.layers.Dense(17, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1_c)
    x2 = keras.layers.Dense(17, activation="elu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x2_c)
    x3 = keras.layers.Dense(17, activation="gelu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x3_c)
    x4 = keras.layers.Dense(17, activation="leaky_relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x4_c)
    
    x1 = keras.layers.Dropout(0.5)(x1)
    x2 = keras.layers.Dropout(0.5)(x2)
    x3 = keras.layers.Dropout(0.5)(x3)
    x4 = keras.layers.Dropout(0.5)(x4)
    x5 = keras.layers.BatchNormalization()(x9)
    x6 = keras.layers.Dense(18, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x6)
    x7 = keras.layers.Dense(18, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x4)
    x8 = keras.layers.Dense(18, activation="swish", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x8)  

    x_2_1 =  keras.layers.Concatenate()([x1, x5])
    x_2_2 =  keras.layers.Concatenate()([x2, x6])
    x_2_3 =  keras.layers.Concatenate()([x3, x7])
    x_2_4 =  keras.layers.Concatenate()([x4, x8])
    x_2_1 = keras.layers.Dropout(0.5)(x_2_1)
    x_2_2 = keras.layers.Dropout(0.5)(x_2_2)
    x_2_3 = keras.layers.Dropout(0.5)(x_2_3)
    x_2_4 = keras.layers.Dropout(0.5)(x_2_4)

    x_2_1 =  keras.layers.Dense(12, activation="celu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x_2_1)
    x_2_2 =  keras.layers.Dense(12, activation="glu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x_2_2)
    x_2_3 =  keras.layers.Dense(12, activation="silu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x_2_3)
    x_2_4 =  keras.layers.Dense(12, activation="sigmoid", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x_2_4)
    x_2_1 = keras.layers.Dropout(0.5)(x_2_1)
    x_2_2 = keras.layers.Dropout(0.5)(x_2_2)
    x_2_3 = keras.layers.Dropout(0.5)(x_2_3)
    x_2_4 = keras.layers.Dropout(0.5)(x_2_4)

    x1 = keras.layers.Concatenate()([x_2_1, x_2_3])
    x2 = keras.layers.Concatenate()([x_2_2, x_2_4])

    x1 =  keras.layers.Dense(12, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1)
    x2 =  keras.layers.Dense(12, activation="relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x2)


    x1 = keras.layers.Concatenate()([x1, x2])

    x1 = keras.layers.Dense(12, activation="leaky_relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1)

    x1 = keras.layers.Dropout(0.5)(x1)

    x1 = keras.layers.Dense(6, activation="leaky_relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1)



    x1 = keras.layers.Dense(3, activation="leaky_relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1)



    x1 = keras.layers.Dense(2, activation="leaky_relu", kernel_regularizer=keras.regularizers.L1L2(l1=1e-6, l2=5e-6),activity_regularizer=keras.regularizers.L2(3e-6))(x1)



    outputs = keras.layers.Dense(1)(x1)
    model = keras.Model(inputs, outputs)
    return model








model = build_model(16)


model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.0000015, momentum=0.9),
              loss=keras.losses.MeanSquaredError(),
              metrics=["accuracy"])




# import pandas as pd

# df = pd.read_csv('csv_s/turnModel.csv')

# print(df.to_string()) 


x = []
y = []

# Open the CSV file in read mode
with open('csv_s/turnModel.csv', 'r') as csvfile:
  # Create a reader object
  csv_reader = csv.reader(csvfile, delimiter=";")
  next(csv_reader)
  # Iterate through the rows in the CSV file
  for row in csv_reader:
    x.append(row[:-1])
    y.append(row[-1])

    # Access each element in the row

x2 = []
for input_ in x:
   x2.append(np.array(list(map(float, input_))))

x2 = np.array(x2)
y = np.array(list(map(float, y)))

for input_ in x2:
   print(input_)
   print(len(input_))
exit()

# x = np.array(list(map(float, x)))
# y = np.array(list(map(float, y)))

# print(str(x2))
# print(str(y))
# exit()



model.fit(x2, y, epochs=50, batch_size=batch_size,
           # callbacks=..., 
           # validation_data=...
           )














