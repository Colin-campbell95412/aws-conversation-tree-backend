from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .dynamodb import *
from .jwt_utils import generate_jwt
from .auth import token_required

@csrf_exempt
def signup(request):
    
    if request.method == 'POST':
        
        # data = json.loads(request.body)
        data = request.POST.dict()  # Assuming request.POST is a dictionary
        print('Data:', data)
        if data.get('user_id'):
            print('Updating user:', data)
            update_user(data['user_id'], {'password': data['password'], 'username': data['username']})
            return JsonResponse({
                'status': 'success',
                'message': 'User updated successfully',
                # 'data': {
                #     'msg': 'User updated successfully'
                # }
            })
        else:
            print('Creating user:', data)
            if get_user(data['username']):
                # return JsonResponse({'error': 'Username already exists'}, status=400)
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Username already exists'
                    # 'data': {
                    #     'msg': 'Username already exists'
                    # }
                })
            print('Creating user:', data)
            create_user(data['username'], data['password'])
            return JsonResponse({
                'status': 'success',
                'message': 'User created successfully',
            })

@csrf_exempt
def login(request):
    print('Login request:', request.POST)
    if request.method == 'POST':
        data = request.POST.dict()
        user = get_user(data['username'])
        print('Login request:', request.POST)
        if not user:
            print('User not found:', data['username'])
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        if user and user['password'] == hash_password(data['password']):
            print('User authenticated:', user['username'])
            token = generate_jwt(user['username'])
            # print('Generated token:', token)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'user_info': user,
                    'token': token
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

@csrf_exempt
@token_required
def logout(request):
    return JsonResponse({'message': 'Logged out'})  # Stateless logout

@token_required
def get_users(request):
    print('Get users request:', request.method)
    if request.method == 'GET':
        print('Fetching all users')
        users = get_all_users()
        data = {
            'status': "success",
            'data': users
        }
        return JsonResponse(data, safe=False)

@csrf_exempt
@token_required
def update_user_view(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_user(user_id, data)
        return JsonResponse({'message': 'User updated'})

@csrf_exempt
@token_required
def delete_user_view(request, user_id):
    if request.method == 'DELETE':
        delete_user(user_id)
        return JsonResponse({
            'status': 'success',
            'message': 'User deleted successfully',
        })

@csrf_exempt
@token_required
def bulk_delete_users_view(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        print('Deleting users:', ids)
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid JSON in ids'})
        if isinstance(ids, list):
            for user_id in ids:
                delete_user(user_id)
            return JsonResponse({
            'status': 'success',
            'message': 'Users deleted successfully',
            })
        else:
            return JsonResponse({
            'status': 'fail',
            'message': 'Invalid input',
            })