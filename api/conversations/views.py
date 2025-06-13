from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from .dynamodb import *
from ..users.auth import token_required

@csrf_exempt
@token_required
def add_conversation_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        intro = data.get('introduction')
        tree_str = data.get('conversation_tree')
        id = data.get('id')
        
        try:
            tree = json.loads(tree_str)
        except json.JSONDecodeError:
            try:
                tree = ast.literal_eval(tree_str)
            except Exception as e:
                return JsonResponse({'status': 'fail', 'message': 'Failed to save conversation tree.'})
        if id == '-1':
            add_conversation(intro, tree)
        else:
            update_conversation(id, intro, tree)
        return JsonResponse({
            'status': 'success',
            'message': 'Conversation saved successfully',
        })

@csrf_exempt
@token_required
def delete_conversation_view(request, convo_id):
    if request.method == 'DELETE':
        delete_conversation(convo_id)
        return JsonResponse({'status': 'success', 'message': 'Conversation deleted'})

@token_required
def get_conversation_view(request, convo_id):
    if request.method == 'GET':
        convo = get_conversation(convo_id)
        if convo:
            return JsonResponse({
                'status': 'success',
                'data': convo,
            })
        return JsonResponse({'error': 'Conversation not found'}, status=404)

@token_required
def list_conversations_view(request):
    if request.method == 'GET':
        return JsonResponse({
            'status': 'success',
            'data': list_conversations(),
        })


@csrf_exempt
@token_required
def bulk_delete_conversations_view(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        print('Deleting conversations:', ids)
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid JSON in ids'})
        if isinstance(ids, list):
            for conversation_id in ids:
                delete_conversation(conversation_id)
            return JsonResponse({
            'status': 'success',
            'message': 'Conversations deleted successfully',
            })
        else:
            return JsonResponse({
            'status': 'fail',
            'message': 'Invalid input',
            })