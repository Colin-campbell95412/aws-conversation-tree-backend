import boto3
import hashlib
import uuid
from boto3.dynamodb.conditions import Attr
from libs.dynamodb_client import dynamodb

table = dynamodb.Table('users')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# def create_user(username, password):
def create_user(username, password, role="user"):
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        'username': username,
        'password': hash_password(password),
        'role': role
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
    # Never allow updating the role field
    if 'role' in updates:
        updates.pop('role')
    # Remove empty password or None
    if 'password' in updates:
        print("Updating password for user:", user_id)
        if not updates['password']:
            updates.pop('password')
        else:
            print("Hashing password for user:", user_id)
            updates['password'] = hash_password(updates['password'])
    # Do not proceed if updates is empty
    if not updates:
        print("No updates provided for user:", user_id)
        return
    update_expr = 'SET ' + ', '.join(f"{k}=:{k}" for k in updates)
    expr_vals = {f":{k}": v for k, v in updates.items()}
    table.update_item(
        Key={'id': user_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_vals
    )

def delete_user(user_id):
    table.delete_item(Key={'id': user_id})
