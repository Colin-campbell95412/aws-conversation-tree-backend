import boto3
import hashlib
import uuid
from boto3.dynamodb.conditions import Attr
from libs.dynamodb_client import dynamodb

table = dynamodb.Table('docs')

# def hash_paord(password):
#     return hashlib.sha256(password.encode()).hexdigest()

def create_doc(title, description):
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        'title': title,
        'description': description
    })

def get_all_docs():
    return table.scan().get('Items', [])

def get_doc(title):
    try:
        response = table.scan(
            FilterExpression=Attr('title').eq(title)
        )
        items = response.get('Items', [])
        if items:
            doc = items[0]  # if you're sure it's unique
        else:
            doc = None
    except Exception as e:
        print(f"Error getting doc '{title}': {e}")
        doc = None
    return doc

def update_doc(doc_id, updates: dict):
    # updates['password'] = hash_password(updates['password'])
    update_expr = 'SET ' + ', '.join(f"{k}=:{k}" for k in updates)
    expr_vals = {f":{k}": v for k, v in updates.items()}
    table.update_item(
        Key={'id': doc_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_vals
    )

def delete_doc(doc_id):
    table.delete_item(Key={'id': doc_id})
