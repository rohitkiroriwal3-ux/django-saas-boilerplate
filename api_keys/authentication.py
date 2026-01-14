from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            return None

        if not auth.startswith("Bearer sk_"):
            return None

        key = auth.replace("Bearer ", "")

        try:
            api_key = APIKey.objects.get(key=key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (api_key.organization.owner, None)
