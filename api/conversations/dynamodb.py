import boto3
import uuid

dynamodb = boto3.resource(
        'dynamodb', 
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        endpoint_url='http://localhost:4566' # Local DynamoDB endpoint
    )  # Change region as needed
conversations_table = dynamodb.Table('conversations')

def generate_convo_id():
    return str(uuid.uuid4())

def add_conversation(introduction, conversation_tree):
    convo_id = generate_convo_id()
    conversations_table.put_item(Item={
        'id': convo_id,
        'introduction': introduction,
        'conversation_tree': conversation_tree
    })
    return convo_id

def delete_conversation(convo_id):
    conversations_table.delete_item(Key={'id': convo_id})

def get_conversation(convo_id):
    res = conversations_table.get_item(Key={'id': convo_id})
    return res.get('Item')

def list_conversations():
    response = conversations_table.scan(ProjectionExpression="id, introduction")
    return response.get('Items', [])
    # return conversations_table.scan().get('Items', [])
def update_conversation(convo_id, introduction=None, conversation_tree=None):
    update_expression = []
    expression_attribute_values = {}

    if introduction is not None:
        update_expression.append("introduction = :intro")
        expression_attribute_values[":intro"] = introduction

    if conversation_tree is not None:
        update_expression.append("conversation_tree = :tree")
        expression_attribute_values[":tree"] = conversation_tree

    if not update_expression:
        raise ValueError("No fields to update")

    conversations_table.update_item(
        Key={'id': convo_id},
        UpdateExpression="SET " + ", ".join(update_expression),
        ExpressionAttributeValues=expression_attribute_values
    )
