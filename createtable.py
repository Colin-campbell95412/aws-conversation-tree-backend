import boto3

def create_users_table():
    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource(
        'dynamodb', 
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        endpoint_url='http://localhost:4566'  # Change endpoint URL as needed
    )  # Change region as needed

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