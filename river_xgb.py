import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
from joblib import dump, load
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# probability_1_1;pdata_average_1;pdata_average_2;pdata_average_3;pdata_average_4;pdata_before_me_1;pdata_before_me_2;pdata_before_me_3;pdata_before_me_4;i_call_preflop;i_bet_preflop;i_call_flop;i_bet_flop;i_call_river;i_bet_river;potheight;potheight_after_preflop;potheight_after_flop;to_call;decision;num_active_players;num_active_players_before_me;feat_1;feat_2;feat_3;feat_4;feat_5;feat_6;feat_7;feat_8;feat_9;feat_10;feat_11;feat_12;feat_13;feat_14;label


inputs = ["probability_1_1","pdata_average_1","pdata_average_2","pdata_average_3","pdata_average_4","pdata_before_me_1","pdata_before_me_2","pdata_before_me_3","pdata_before_me_4","i_call_preflop","i_bet_preflop","i_call_flop","i_bet_flop","i_call_river","i_bet_river","potheight","potheight_after_preflop","potheight_after_flop","to_call","decision","num_active_players","num_active_players_before_me","feat_1","feat_2","feat_3","feat_4","feat_5","feat_6","feat_7","feat_8","feat_9","feat_10","feat_11","feat_12","feat_13","feat_14"]
# Load data
df = pd.read_csv('csv_s/riverModel.csv', sep=';')
X = df[inputs].values
y = df['label'].values.astype(float)

# Normalize inputs to [0, 1] (assuming they are in [0, 2] as per your note)
# print(X[0])
# exit()
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

with open(f"river_model_scaler", "wb") as fp:   #Pickling      
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


dump(model, "river_xgb.joblib")    


# y_pred = model.predict(X_test)

# print(y_pred[:10])

# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# mae = mean_absolute_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print("RMSE:", rmse)
# print("MAE:", mae)
# print("R²:", r2)




