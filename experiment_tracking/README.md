*Experiment Tracking* is a process of keeping track of all the relevant information from an ml experiment which includes source code , models , enviornment , hyperparameters , metrics 
first, create a conda env and activate it 

then, install the requirements : pip install-r requirements.txt

run the mlflow ui : 
mlflow ui --backend-store-uri sqlite:///mlflow.db

at last , experiment in the notebook .

