import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SNS client in us-west-2
sns = boto3.client('sns', region_name='us-west-2')

# Topic and webhook details
topic_name = 'DeploymentSuccess'
webhook_url = 'https://hooks.slack.com/services/your/webhook/url'  # Replace with your actual Slack webhook

def create_topic(name):
    try:
        response = sns.create_topic(Name=name)
        topic_arn = response['TopicArn']
        logger.info(f"✅ Created topic '{name}': {topic_arn}")
        return topic_arn
    except (BotoCoreError, ClientError) as error:
        logger.error(f"❌ Failed to create topic '{name}': {error}")
        return None

def subscribe_webhook(topic_arn, endpoint):
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='https',
            Endpoint=endpoint
        )
        logger.info(f"✅ Subscribed webhook to topic: {response['SubscriptionArn']}")
    except (BotoCoreError, ClientError) as error:
        logger.error(f"❌ Failed to subscribe webhook: {error}")

def main():
    topic_arn = create_topic(topic_name)
    if topic_arn:
        subscribe_webhook(topic_arn, webhook_url)
    else:
        logger.warning("⚠️ Skipping subscription due to topic creation failure.")

if __name__ == "__main__":
    main()
