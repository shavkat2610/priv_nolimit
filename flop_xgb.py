import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
from joblib import dump, load
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score





inputs = ['equity_flop', 'potheight', 'average_pot_2', 'average_pot_3', 'average_pot_4', 'average_pot_5', 'average_pot_6', 'average_pot_7', 'average_pot_9', 'average_pot_11', 'average_pot_13', 'average_pot_16', 'average_pot_20', 'average_pot_30', 'average_pot_50', 'to_call', 'decision', 'difference_tocall_n_potheight', 'flop_feat_1', 'flop_feat_2', 'flop_feat_3', 'flop_feat_4', 'flop_feat_5', 'flop_feat_6', 'flop_feat_7', 'flop_feat_8', 'flop_feat_9', 'flop_feat_10', 'flop_feat_11', 'flop_feat_12', 'flop_feat_13', 'flop_feat_14', 'flop_feat_15', 'flop_feat_16', 'flop_feat_17', 'flop_feat_18', 'flop_feat_19', 'flop_feat_20', 'flop_feat_21', 'flop_feat_22', 'flop_feat_23', 'flop_feat_24', 'flop_feat_25', 'flop_feat_26', 'flop_feat_27', 'flop_feat_28', 'flop_feat_29', 'flop_feat_30', 'flop_feat_31', 'flop_feat_32']
# Load data

# print(len(inputs))
# exit()

df = pd.read_csv('csv_s/flopModel.csv', sep=';')
X = df[inputs].values
y = df['label'].values.astype(float)

# Normalize inputs to [0, 1] (assuming they are in [0, 2] as per your note)
# print(X[0])
# exit()
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

with open(f"flop_model_scaler", "wb") as fp:   #Pickling      
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


dump(model, "flop_xgb.joblib")    


# y_pred = model.predict(X_test)

# print(y_pred[:10])

# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# mae = mean_absolute_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print("RMSE:", rmse)
# print("MAE:", mae)
# print("R²:", r2)





































































































































































































































