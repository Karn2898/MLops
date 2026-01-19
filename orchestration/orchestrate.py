from prefect import flow, task
from datetime import datetime
import pandas as pd
import pickle
import mlflow
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import numpy as np

@task
def read_data(filename: str):
    """Read parquet file and prepare data"""
    df = pd.read_parquet(filename)
    
    df['duration'] = (df.lpep_dropoff_datetime - df.lpep_pickup_datetime).dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df

@task
def prepare_features(df_train, df_val):
    """Prepare features using DictVectorizer"""
    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']
    
    dv = DictVectorizer()
    
    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)
    
    val_dicts = df_val[categorical + numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts)
    
    y_train = df_train['duration'].values
    y_val = df_val['duration'].values
    
    return X_train, X_val, y_train, y_val, dv

@task
def train_model(X_train, X_val, y_train, y_val, dv):
    """Train XGBoost model and log to MLflow"""
    
    mlflow.set_tracking_uri('sqlite:///mlflow.db')
    mlflow.set_experiment("nyc-taxi-prefect")
    
    train_data = xgb.DMatrix(X_train, label=y_train)
    val_data = xgb.DMatrix(X_val, label=y_val)
    
    params = {
        'max_depth': 6,
        'learning_rate': 0.1,
        'objective': 'reg:squarederror',
        'seed': 42
    }
    
    with mlflow.start_run():
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(params)
        
        booster = xgb.train(
            params=params,
            dtrain=train_data,
            num_boost_round=100,
            evals=[(val_data, 'validation')],
            early_stopping_rounds=10,
            verbose_eval=False
        )
        
        y_pred = booster.predict(val_data)
        rmse = np.sqrt(mean_squared_error(y_val, y_pred))
        
        mlflow.log_metric("rmse", rmse)
        
      
        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")
        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
        
        print(f"RMSE: {rmse:.4f}")
        return rmse

@flow
def main_flow(train_path: str, val_path: str):
    
    df_train = read_data(train_path)
    df_val = read_data(val_path)
    
    X_train, X_val, y_train, y_val, dv = prepare_features(df_train, df_val)
    
    
    rmse = train_model(X_train, X_val, y_train, y_val, dv)
    
    print(f" Workflow completed! RMSE: {rmse:.4f}")

if __name__ == "__main__":
    train_path = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet"
    val_path = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-02.parquet"
    
    main_flow(train_path, val_path)