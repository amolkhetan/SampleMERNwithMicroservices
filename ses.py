import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sns = boto3.client('sns', region_name='us-west-2')

failure_topic_arn = 'arn:aws:sns:us-west-2:123456789012:DeploymentFailure'  # Replace with your actual ARN
email_endpoint = 'amol.khetan@gmail.com'

try:
    response = sns.subscribe(
        TopicArn=failure_topic_arn,
        Protocol='email',
        Endpoint=email_endpoint
    )
    logger.info(f"✅ Email subscription created: {response['SubscriptionArn']}")
    print(f"Subscription ARN: {response['SubscriptionArn']}")
except (BotoCoreError, ClientError) as error:
    logger.error(f"❌ Failed to subscribe email to topic: {error}")
    print(f"Error: {error}")
