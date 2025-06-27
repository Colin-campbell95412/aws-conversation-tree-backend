from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .dynamodb import *
# from .jwt_utils import generate_jwt
from ..users.auth import token_required

@csrf_exempt
def add_or_edit_doc_view(request):
    
    if request.method == 'POST':
        
        # data = json.loads(request.body)
        data = request.POST.dict()  # Assuming request.POST is a dictionary
        print('Data:', data)
        if data.get('doc_id'):
            print('Updating doc:', data)
            update_doc(data['doc_id'], {'description': data['description'], 'title': data['title']})
            return JsonResponse({
                'status': 'success',
                'message': 'Doc updated successfully',
            })
        else:
            print('Creating doc:', data)
            if get_doc(data['title']):
                return JsonResponse({
                    'status': 'fail',
                    'message': 'This title already exists'
                })
            print('Creating doc:', data)
            create_doc(data['title'], data['description'])
            return JsonResponse({
                'status': 'success',
                'message': 'Doc created successfully',
            })

@token_required
def get_docs(request):
    print('Get docs request:', request.method)
    if request.method == 'GET':
        print('Fetching all docs')
        docs = get_all_docs()
        data = {
            'status': "success",
            'data': docs
        }
        return JsonResponse(data, safe=False)

@csrf_exempt
@token_required
def update_doc_view(request, doc_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        update_doc(doc_id, data)
        return JsonResponse({'message': 'Doc updated'})

@csrf_exempt
@token_required
def delete_doc_view(request, doc_id):
    if request.method == 'DELETE':
        delete_doc(doc_id)
        return JsonResponse({
            'status': 'success',
            'message': 'Doc deleted successfully',
        })

@csrf_exempt
@token_required
def bulk_delete_docs_view(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        print('Deleting docs:', ids)
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'fail', 'message': 'Invalid JSON in ids'})
        if isinstance(ids, list):
            for doc_id in ids:
                delete_doc(doc_id)
            return JsonResponse({
            'status': 'success',
            'message': 'Docs deleted successfully',
            })
        else:
            return JsonResponse({
            'status': 'fail',
            'message': 'Invalid input',
            })