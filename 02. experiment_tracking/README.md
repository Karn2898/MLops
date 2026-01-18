1.**Experiment Tracking** is a process of keeping track of all the relevant information from an ml experiment which includes source code , models , enviornment , hyperparameters , metrics 
first, create a conda env and activate it 

then, install the requirements : pip install-r requirements.txt

run the mlflow ui : 
mlflow ui --backend-store-uri sqlite:///mlflow.db

at last , experiment in the notebook .

2. **model management**:

either save the model in mlflow using mlflow.log_artifact(local_path ='',artifact_path='')

or, 

i) copy paste training loop from any used framework in the notebook 

ii) add log_params 

iii) add log_model in the end 

logged_model=''

**load model as pyfunmodel**
