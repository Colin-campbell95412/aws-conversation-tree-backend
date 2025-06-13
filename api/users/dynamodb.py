import boto3
import hashlib
import uuid
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource(
        'dynamodb', 
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        endpoint_url='http://localhost:4566' # Local DynamoDB endpoint
    )  # Change region as needed

table = dynamodb.Table('users')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        'username': username,
        'password': hash_password(password)
    })

def get_all_users():
    return table.scan().get('Items', [])

def get_user(username):
    try:
        response = table.scan(
            FilterExpression=Attr('username').eq(username)
        )
        items = response.get('Items', [])
        if items:
            user = items[0]  # if you're sure it's unique
        else:
            user = None
    except Exception as e:
        print(f"Error getting user '{username}': {e}")
        user = None
    return user

def update_user(user_id, updates: dict):
    updates['password'] = hash_password(updates['password'])
    update_expr = 'SET ' + ', '.join(f"{k}=:{k}" for k in updates)
    expr_vals = {f":{k}": v for k, v in updates.items()}
    table.update_item(
        Key={'id': user_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_vals
    )

def delete_user(user_id):
    table.delete_item(Key={'id': user_id})
