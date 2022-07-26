import json
import boto3
import time

batch = boto3.client('batch')


def lambda_handler(event, context):

    step = event['Step']
    print(f'Running {step} batch job...')
    submit_job_response = batch.submit_job(
        jobName=f'JB-COST-ANOMALY-{step}',
        jobQueue='JQ-COST-ANOMALY-BATCH',
        jobDefinition=f'JD-DEV-COST-ANOMALY-{step}',
    )

    jobId = submit_job_response['jobId']
    jobArn = submit_job_response['jobArn']

    event['jobId'] = jobId
    event['jobArn'] = jobArn

    max_time = time.time() + 10*60  # 10 min
    while time.time() < max_time:
        describe_jobs_response = batch.describe_jobs(jobs=[jobId])
        status = describe_jobs_response['jobs'][0]['status']
        print(f'BatchJob: {status}')

        if (status == 'SUCCEEDED') or (status == 'FAILED'):
            break

        time.sleep(60)

    if (status == 'SUCCEEDED') or (status == 'FAILED'):
        event['status'] = status
        return event
    else:
        raise Exception('TIMEOUT')
