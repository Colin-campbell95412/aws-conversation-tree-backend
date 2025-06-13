from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .dynamodb import *
# from .jwt_utils import generate_jwt
from ..users.auth import token_required

@csrf_exempt
def add_or_edit_lab_view(request):
    
    if request.method == 'POST':
        
        # data = json.loads(request.body)
        data = request.POST.dict()  # Assuming request.POST is a dictionary
        print('Data:', data)
        if data.get('lab_id'):
            print('Updating lab:', data)
            update_lab(data['lab_id'], {'description': data['description'], 'title': data['title']})
            return JsonResponse({
                'status': 'success',
                'message': 'lab updated successfully',
            })
        else:
            print('Creating lab:', data)
            if get_lab(data['title']):
                return JsonResponse({
                    'status': 'fail',
                    'message': 'This title already exists'
                })
            print('Creating lab:', data)
            create_lab(data['title'], data['description'])
            return JsonResponse({
                'status': 'success',
                'message': 'Lab created successfully',
            })

@token_required
def get_labs(request):
    print('Get labs request:', request.method)
    if request.method == 'GET':
        print('Fetching all labs')
        labs = get_all_labs()
        data = {
            'status': "success",
            'data': labs
        }
        return JsonResponse(data, safe=False)

@csrf_exempt
@token_required
def update_lab_view(request, lab_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_lab(lab_id, data)
        return JsonResponse({'message': 'Lab updated'})

@csrf_exempt
@token_required
def delete_lab_view(request, lab_id):
    if request.method == 'DELETE':
        delete_lab(lab_id)
        return JsonResponse({
            'status': 'success',
            'message': 'Lab deleted successfully',
        })

@csrf_exempt
@token_required
def bulk_delete_labs_view(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        print('Deleting labs:', ids)
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid JSON in ids'})
        if isinstance(ids, list):
            for lab_id in ids:
                delete_lab(lab_id)
            return JsonResponse({
            'status': 'success',
            'message': 'Labs deleted successfully',
            })
        else:
            return JsonResponse({
            'status': 'fail',
            'message': 'Invalid input',
            })