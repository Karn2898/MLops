# Prefect Cloud Deployment Guide

## Prerequisites
- Prefect account at https://app.prefect.cloud
- API key from your Prefect Cloud account

## Setup Steps

### 1. Authenticate with Prefect Cloud
```bash
prefect cloud login
```
When prompted, paste your API key from https://app.prefect.cloud/account/api-keys

### 2. Create a Work Pool
```bash
prefect work-pool create --type process process-work-pool
```

Or go to https://app.prefect.cloud and create manually:
- Click "Work Pools"
- Click "Create Work Pool"
- Select "Process" type
- Name it `process-work-pool`

### 3. Deploy Flows
```bash
cd /workspaces/MLops/orchestration
prefect deploy
```

This will create three deployments:
- `monthly-training`: Scheduled to run monthly training
- `backfill-training`: For backfilling historical data
- `hello-world`: Simple test flow

### 4. Start a Worker
In a separate terminal, start a worker to execute your flows:
```bash
prefect worker start -p process-work-pool
```

The worker will continuously poll for scheduled runs and execute them.

## Triggering Flows Manually
```bash
# Run a specific deployment
prefect deployment run "monthly-training/monthly-training"

# Run backfill with specific parameters
prefect deployment run "backfill-training/backfill-training" \
  -p start_year=2021 \
  -p start_month=1 \
  -p end_year=2021 \
  -p end_month=6
```

## Monitoring
- View flow runs: https://app.prefect.cloud
- Check worker status: `prefect worker list`
- View work pools: `prefect work-pool list`

## Troubleshooting

### "No workspaces found" error
- Make sure you created a workspace at https://app.prefect.cloud

### Worker not executing flows
- Ensure worker is running: `prefect worker start -p process-work-pool`
- Check work pool name matches in `prefect.yaml`

### Flows not appearing in Cloud
- Verify you're logged in: `prefect config view`
- Check your API key is valid
- Rerun deployment: `prefect deploy`
