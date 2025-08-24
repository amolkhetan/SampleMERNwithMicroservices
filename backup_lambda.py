import boto3
import datetime
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'your-backup-bucket'
    db_dump_path = '/tmp/db-backup.sql'  # or .gz, .json, etc.

    # Simulate DB dump (replace with actual dump command if needed)
    with open(db_dump_path, 'w') as f:
        f.write('Sample DB backup content')

    # Timestamped filename
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    s3_key = f"backups/db-backup-{timestamp}.sql"

    # Upload to S3
    s3.upload_file(db_dump_path, bucket_name, s3_key)

    return {
        'statusCode': 200,
        'body': f"Backup uploaded to s3://{bucket_name}/{s3_key}"
    }
