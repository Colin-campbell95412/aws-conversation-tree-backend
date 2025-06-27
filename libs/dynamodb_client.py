import boto3
import os

USE_LOCAL_DYNAMODB = os.getenv("USE_LOCAL_DYNAMODB", "false").lower() == "true"

if USE_LOCAL_DYNAMODB:
    # Local testing (DynamoDB Local)
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test" # Use test credentials for local testing
    )
else:
    # Production (real AWS DynamoDB via Gateway Endpoint or public access)
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="eu-north-1"				# "us-southeast-2"  # Your AWS region
        # No endpoint_url needed
    )