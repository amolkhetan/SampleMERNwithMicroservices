import boto3
import os
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')

def lambda_handler(event, context):
    status = event.get('deployment_status')
    message = event.get('message', 'No message provided')

    if not status:
        logger.error("❌ 'deployment_status' not found in event.")
        return {'statusCode': 400, 'body': "Missing deployment_status"}

    topic_env_var = 'SUCCESS_TOPIC_ARN' if status == 'success' else 'FAILURE_TOPIC_ARN'
    topic_arn = os.environ.get(topic_env_var)

    if not topic_arn:
        logger.error(f"❌ Environment variable '{topic_env_var}' not set.")
        return {'statusCode': 500, 'body': f"Missing topic ARN for {status} status"}

    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=f"Deployment {status.capitalize()}"
        )
        logger.info(f"✅ Notification sent to {status} topic: {response['MessageId']}")
        return {'statusCode': 200, 'body': f"Notification sent to {status} topic"}
    except (BotoCoreError, ClientError) as error:
        logger.error(f"❌ Failed to publish to SNS topic: {error}")
        return {'statusCode': 500, 'body': "Failed to send notification"}
