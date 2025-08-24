import boto3

lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

# IAM Role ARN with Lambda + S3 permissions
role_arn = 'arn:aws:iam::975050024946:role/LambdaS3ExecutionRole'

# Read zipped Lambda code
with open('backup_lambda.zip', 'rb') as f:
    zipped_code = f.read()

# Create Lambda function
response = lambda_client.create_function(
    FunctionName='DBBackupFunction',
    Runtime='python3.9',
    Role=role_arn,
    Handler='backup_lambda.lambda_handler',
    Code={'ZipFile': zipped_code},
    Timeout=300,
    MemorySize=128,
    Publish=True
)

print(f"✅ Lambda function created: {response['FunctionArn']}")
