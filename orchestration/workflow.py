from prefect import flow, task
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@task
def main_flow(train_path: str, val_path: str):

    pass


@flow
def monthly_training_flow(run_date: datetime = datetime.now()):
   
    if run_date is None:
        run_date = datetime.now()
    
    
    train_date = run_date - relativedelta(months=2)
    val_date = run_date - relativedelta(months=1)
    
   
    train_path = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{train_date.year}-{train_date.month:02d}.parquet"
    val_path = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{val_date.year}-{val_date.month:02d}.parquet"
    
    print(f"Training with:")
    print(f"  Train: {train_path}")
    print(f"  Val: {val_path}")
    
   
    main_flow(train_path, val_path)

if __name__ == "__main__":
    
    monthly_training_flow()
    
    # Serve the flow with a schedule
    monthly_training_flow.serve(
        name="monthly-taxi-training",
        cron="0 0 1 * *"  # Run at midnight on the 1st of each month
    )