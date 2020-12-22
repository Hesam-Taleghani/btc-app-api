from rest_framework import generics, authentication, permissions
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """retrieving and editing profile for authenticated admins"""
    serializer_class = AdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return the authenticated admin"""
        return self.request.user
