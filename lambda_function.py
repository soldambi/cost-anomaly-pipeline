from exceptions import *
from datetime import datetime, timedelta

import json
import boto3
import time

batch = boto3.client('batch')

jobName = 'JB-COST-ANOMALY-{step}-{date}'
jobQueue = 'JQ-COST-ANOMALY-BATCH'
jobDefinition = 'JD-DEV-COST-ANOMALY-{step}'


def lambda_handler(event, context):

    step = event['step']
    print(f'This step is {step} step.')

    date = event['time'].replace(':', '-')
    if date[-1] == 'Z':
        utc_datetime_obj = datetime.strptime(date, '%Y-%m-%dT%H-%M-%SZ')
        kst_datetime_obj = utc_datetime_obj + timedelta(hours=9)
        date = datetime.strftime(kst_datetime_obj, '%Y-%m-%dT%H-%M-%SK')

    list_jobs_response = batch.list_jobs(
        jobQueue=jobQueue,
        filters=[
            {
                'name': 'JOB_NAME',
                'values': [
                    jobName.format(step=step, date=date)
                ]
            },
        ]
    )
    if list_jobs_response['jobSummaryList']:
        print(f'Already submitted {step} batch job...')
        job = list_jobs_response['jobSummaryList'][0]
        status = job['status']
    else:
        print(f'Submitting {step} batch job...')
        submit_job_response = batch.submit_job(
            jobName=jobName.format(step=step, date=date),
            jobQueue=jobQueue,
            jobDefinition=jobDefinition.format(step=step)
        )
        status = 'SUBMITTED'

    print(f'Status: {status}')
    if status == 'SUCCEEDED':
        event['status'] = status
        event['time'] = date
        return event
    elif status == 'FAILED':
        raise ResourceFailed(step, status)
    else:
        raise ResourcePending(step, status)
