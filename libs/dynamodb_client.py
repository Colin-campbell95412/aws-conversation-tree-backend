import boto3
import os

USE_LOCAL_DYNAMODB = os.getenv("USE_LOCAL_DYNAMODB", "false").lower() == "true"

if USE_LOCAL_DYNAMODB:
    # Local testing (DynamoDB Local)
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="ap-southeast-2",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy"
    )
else:
    # Production (real AWS DynamoDB via Gateway Endpoint or public access)
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="ap-southeast-2"  # Your AWS region
        # No endpoint_url needed
    )