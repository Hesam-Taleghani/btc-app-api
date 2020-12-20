from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from admins.serializers import AdminSerializer, AuthTokenSerializer

class CreateAdminView(generics.CreateAPIView):
    """Create a new admin"""
    serializer_class = AdminSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a token for loged in admin"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES