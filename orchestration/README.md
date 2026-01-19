
**ML pipeline** refers to sequence of steps we execute in order to train a model.

I converted the .ipynb file (the notebook) into a .py file (python script), for that just check ridetime_prediction.ipynb 

mlflow command : mlflow server \
    --backend-store-uri sqlite:///mlflow.db


data url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet'
=======
to run the .py file : python /workspaces/MLops/orchestration/ridetime_prediction.py --year2021 --month=1


3. **using orchestration:**
1. # Install
pip install prefect python-dateutil
2. single training run of .py script
python ridetime_prediction_prefect.py --mode train --year 2021 --month 1
# Test hello world
python test_prefect.py

# Run orchestrated workflow
python orchestrate_ml.py

3. Create scheduled deployment
python scheduled_workflow.py

4. Backfill historical data

# Install
pip install prefect python-dateutil

# Test hello world
python test_prefect.py

# Run orchestrated workflow
python orchestrate_ml.py

# Create scheduled deployment
python scheduled_workflow.py

# Backfill historical data
python backfill.py

# Start Prefect UI
prefect server start


6. Start Prefect UI
prefect server start



