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

table = dynamodb.Table('labs')

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

def create_lab(title, description):
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        'title': title,
        'description': description
    })

def get_all_labs():
    return table.scan().get('Items', [])

def get_lab(title):
    try:
        response = table.scan(
            FilterExpression=Attr('title').eq(title)
        )
        items = response.get('Items', [])
        if items:
            lab = items[0]  # if you're sure it's unique
        else:
            lab = None
    except Exception as e:
        print(f"Error getting lab '{title}': {e}")
        lab = None
    return lab

def update_lab(lab_id, updates: dict):
    # updates['password'] = hash_password(updates['password'])
    update_expr = 'SET ' + ', '.join(f"{k}=:{k}" for k in updates)
    expr_vals = {f":{k}": v for k, v in updates.items()}
    table.update_item(
        Key={'id': lab_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_vals
    )

def delete_lab(lab_id):
    table.delete_item(Key={'id': lab_id})
