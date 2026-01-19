import mlflow
import pickle
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from flask import Flask, request, jsonify


mlflow.set_tracking_uri("sqlite:///mlflow.db")



df = pd.read_parquet('/workspaces/MLops/04 deployment/web_services_mlflow/yellow_tripdata_2025-01.parquet')  


df['duration'] = (df.tpep_dropoff_datetime - df.tpep_pickup_datetime).dt.total_seconds() / 60
df = df[(df.duration >= 1) & (df.duration <= 60)]
df['PU_DO'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)


categorical = ['PU_DO']
numerical = ['trip_distance']

dv = DictVectorizer()
train_dicts = df[categorical + numerical].to_dict(orient='records')
X_train = dv.fit_transform(train_dicts)
y_train = df['duration'].values


with mlflow.start_run():
    model = LinearRegression()
    model.fit(X_train, y_train)

    mlflow.sklearn.log_model(model, "model")
    
 
    with open("preprocessor.b", "wb") as f:
        pickle.dump(dv, f)
    mlflow.log_artifact("preprocessor.b", artifact_path="preprocessor")
    
    RUN_ID = mlflow.active_run().info.run_id
    print(f"Model logged with run_id: {RUN_ID}")


model = mlflow.pyfunc.load_model(f"runs:/{RUN_ID}/model")
with open("preprocessor.b", "rb") as f:
    dv = pickle.load(f)


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    X = dv.transform([features])
    preds = model.predict(X)
    return float(preds[0])

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)
    
    result = {
        'duration': pred,
        'model_version': RUN_ID
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)