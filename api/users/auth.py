from django.http import JsonResponse
from .jwt_utils import decode_jwt
from .dynamodb import get_user

def token_required(view_func):
    # print('Token required decorator initialized')
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization token missing'}, status=401)
        token = auth.split()[1]
        # print('Authorization token:', token)
        username = decode_jwt(token)
        if not username:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        user = get_user(username)
        if not user:
            print('User not found: %s', username)
            return JsonResponse({'error': 'User not found'}, status=404)
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper