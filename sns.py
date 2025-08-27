import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sns = boto3.client('sns')

def create_topic(name):
    try:
        response = sns.create_topic(Name=name)
        topic_arn = response['TopicArn']
        logger.info(f"✅ Successfully created topic '{name}': {topic_arn}")
        return topic_arn
    except (BotoCoreError, ClientError) as error:
        logger.error(f"❌ Failed to create topic '{name}': {error}")
        return None

# Create topics
success_topic_arn = create_topic('DeploymentSuccess-amk')
failure_topic_arn = create_topic('DeploymentFailure-amk')

# Optional: Confirm both topics were created
if success_topic_arn and failure_topic_arn:
    logger.info("🎯 All topics created successfully.")
else:
    logger.warning("⚠️ One or more topics failed to create.")
