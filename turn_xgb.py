import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
from joblib import dump, load
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score





inputs = ['probability_1_1', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_4', 'average_pot_5', 'average_pot_6', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'equity_flop', 'equity_river', 'decision', 'difference_tocall_n_potheight']
# Load data
df = pd.read_csv('csv_s/turnModel.csv', sep=';')
X = df[inputs].values
y = df['label'].values.astype(float)

# Normalize inputs to [0, 1] (assuming they are in [0, 2] as per your note)
# print(X[0])
# exit()
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

with open(f"turn_model_scaler", "wb") as fp:   #Pickling      
    pickle.dump(scaler, fp) 

# Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = xgb.XGBRegressor(
    n_estimators=25000,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8
)

model.fit(X, y)


dump(model, "turn_xgb.joblib")    


# y_pred = model.predict(X_test)

# print(y_pred[:10])

# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# mae = mean_absolute_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print("RMSE:", rmse)
# print("MAE:", mae)
# print("R²:", r2)




