from prefect import flow, task
from datetime import datetime
from dateutil.relativedelta import relativedelta
import subprocess
import sys

@task
def run_training(year: int, month: int):
    """Run the training pipeline for a specific year and month"""
    result = subprocess.run(
        [sys.executable, "ridetime_prediction.py", "--train", "--year", str(year), "--month", str(month)],
        cwd="/workspaces/MLops/orchestration",
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error training for {year}-{month:02d}:")
        print(result.stderr)
        raise Exception(f"Training failed for {year}-{month:02d}")
    print(result.stdout)
    return result.stdout

@flow
def monthly_training_flow(run_date: datetime):
    """Flow to train the model for a specific month"""
    year = run_date.year
    month = run_date.month
    print(f"Training flow starting for {year}-{month:02d}")
    output = run_training(year=year, month=month)
    return output

@flow
def backfill_training(start_year: int, start_month: int, end_year: int, end_month: int):
  
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    
    current_date = start_date
    
    while current_date <= end_date:
        print(f"\n{'='*50}")
        print(f"Running for {current_date.strftime('%Y-%m')}")
        print(f"{'='*50}")
        
        monthly_training_flow(run_date=current_date)
        
        current_date += relativedelta(months=1)
    
    print("\n Backfill completed!")

if __name__ == "__main__":
   
    backfill_training(
        start_year=2021,
        start_month=3,
        end_year=2021,
        end_month=6
    )