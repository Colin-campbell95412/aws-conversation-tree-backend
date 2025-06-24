from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .dynamodb import *
from ..users.auth import token_required

@csrf_exempt
def add_or_edit_message_view(request):
    if request.method == 'POST':
        data = request.POST.dict() # Assuming request.POST is a dictionary
        print('Data:', data)
        if data.get('message_id'):
            update_message(data['message_id'], {'description': data['description'], 'title': data['title'], 'user_ids': data.get('user_ids', [])})
            print('Updated message:', data)
            return JsonResponse({
                'status': 'success',
                'message': 'Message updated successfully',
            })
        else:
            if get_message(data['title']):
                return JsonResponse({
                    'status': 'fail',
                    'message': 'This title already exists'
                })
            create_message(data['title'], data['description'], data['user_ids'])
            print('Created message:', data)
            return JsonResponse({
                'status': 'success',
                'message': 'Message created successfully',
            })
        
@token_required
def get_messages(request):
    if request.method == 'GET':
        print('Fetching all messages: method::', request.method)
        messages = get_all_messages()
        user = request.user
        # If admin, return all messages
        if user.get('role', 'user') == 'admin':
            filtered_messages = messages
        else:
            # Only return messages where user's id is in user_ids
            user_id = user.get('id')
            filtered_messages = [msg for msg in messages if user_id and user_id in msg.get('user_ids', [])]
        data = {
            'status': "success",
            'data': filtered_messages
        }
        return JsonResponse(data, safe=False)
    
@csrf_exempt
@token_required
def update_message_view(request, message_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_message(message_id, data)
        return JsonResponse({'message': 'Message updated'})
    
@csrf_exempt
@token_required
def delete_message_view(request, message_id):
    if request.method == 'DELETE':
        delete_message(message_id)
        return JsonResponse({'status': 'success', 'message': 'Message deleted successfully'})
    
@csrf_exempt
@token_required
def bulk_delete_messages_view(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        message_ids = data.get('ids', [])
        print('Deleting messages:', message_ids)
        # Handle if ids is a string (e.g., from frontend)
        if isinstance(message_ids, str):
            try:
                message_ids = json.loads(message_ids)
            except Exception:
                return JsonResponse({'status': 'fail', 'message': 'Invalid JSON in ids'})
        if not isinstance(message_ids, list):
            return JsonResponse({'status': 'fail', 'message': 'Invalid input, ids must be a list'})
        try:
            for message_id in message_ids:
                delete_message(message_id)
            return JsonResponse({
                'status': 'success',
                'message': 'Messages deleted successfully',
            })
        except Exception as e:
            print(f"Error deleting messages: {e}")
            return JsonResponse({'status': 'fail', 'message': 'Error deleting messages'})
        
@token_required
def get_message_by_id(request, message_id):
    if request.method == 'GET':
        message = None
        # Assuming you have a get_message_by_id function in dynamodb.py
        from .dynamodb import table
        try:
            response = table.get_item(Key={'id': message_id})
            message = response.get('Item')
        except Exception as e:
            print(f"Error fetching message by id: {e}")
        if message:
            return JsonResponse({'status': 'success', 'data': message})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Message not found'}, status=404)