from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests

class LaravelPassportAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            response = requests.get(
                'https://your-laravel-app.com/api/auth/validate-token',
                headers={'Authorization': auth_header}
            )
            if response.status_code != 200:
                raise AuthenticationFailed('Invalid token')

            user_data = response.json()['data']
            request.user = type('User', (), user_data)  # Mock user with role_id
            return (request.user, None)
        except Exception as e:
            raise AuthenticationFailed('Authentication failed')
