import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import uuid
from libs.dynamodb_client import dynamodb

def add_user_to_dynamodb(table_name, user_info):
    """
    Add user information to an AWS DynamoDB table.

    :param table_name: Name of the DynamoDB table
    :param user_info: Dictionary containing user information
    """
    try:
        # Initialize a DynamoDB resource
        table = dynamodb.Table(table_name)

        # Add user information to the table
        response = table.put_item(Item=user_info)
        print("User added successfully:", response)
    except NoCredentialsError:
        print("AWS credentials not found.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials configuration.")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Example usage
    table_name = "users"  # Replace with your DynamoDB table name
    
    user_info = {
        "id": str(uuid.uuid4()),  # Replace with unique user ID
        "name": "admin",
        "password": "1"
    }

    add_user_to_dynamodb(table_name, user_info)