import boto3
from libs.dynamodb_client import dynamodb

def create_users_table():
    # Initialize a session using Amazon DynamoDB

    # Create the DynamoDB table
    table = dynamodb.create_table(
        TableName='conversations',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'  # String type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='conversations')

    print(f"Table {table.table_name} created successfully.")
    return table

if __name__ == "__main__":
    create_users_table()