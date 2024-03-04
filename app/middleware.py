import jwt
from django.http import JsonResponse
from django.conf import settings


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your JWT validation logic goes here
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer'):
            jwt_token = request.headers.get('Authorization', '').split(' ')[1]
            # Replace 'your_secret_key' with your actual secret key
            secret_key = settings.JWT_SECRET_KEY
            try:
                payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
                request.user_id = payload['name']
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=403)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
            response = self.get_response(request)
            return response
        else:
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=400)
