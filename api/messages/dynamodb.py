import boto3
import hashlib
import uuid
from boto3.dynamodb.conditions import Attr
from libs.dynamodb_client import dynamodb

table = dynamodb.Table('messages')

def create_message(title, description, user_ids=None, to='All'):
    if user_ids is None:
        user_ids = []
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        'title': title,
        'description': description,
        'user_ids': user_ids,
        'to': to
    })

def get_all_messages():
    return table.scan().get('Items', [])

def get_message(title):
    try:
        response = table.scan(
            FilterExpression=Attr('title').eq(title)
        )
        items = response.get('Items', [])
        if items:
            message = items[0]  # if you're sure it's unique
        else:
            message = None
    except Exception as e:
        print(f"Error getting message '{title}': {e}")
        message = None
    return message

def update_message(message_id, updates: dict):
    update_expr_parts = []
    expr_vals = {}
    expr_names = {}
    for k, v in updates.items():
        if k == "to":
            update_expr_parts.append(f"#to=:{k}")
            expr_names["#to"] = "to"
        else:
            update_expr_parts.append(f"{k}=:{k}")
        expr_vals[f":{k}"] = v
    update_expr = 'SET ' + ', '.join(update_expr_parts)
    kwargs = {
        "Key": {'id': message_id},
        "UpdateExpression": update_expr,
        "ExpressionAttributeValues": expr_vals
    }
    if expr_names:
        kwargs["ExpressionAttributeNames"] = expr_names
    table.update_item(**kwargs)

def delete_message(message_id):
    table.delete_item(Key={'id': message_id})
