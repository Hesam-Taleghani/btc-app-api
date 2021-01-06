from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.http import Http404

from admins.serializers import AdminSerializer, AuthTokenSerializer
from core.models import User

class CreateAdminView(generics.CreateAPIView):
    """Create a new admin"""
    serializer_class = AdminSerializer
    permission_classes = (permissions.IsAdminUser,)


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


class ListUsersView(generics.ListAPIView):
    """The viewset to handle admins listing"""
    serializer_class = AdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = get_user_model().objects.all()

    def filter_queryset(self,queryset):
        """To order by name"""
        return self.queryset.order_by('name')


class PromotingAdmin(APIView):
    """The view to manage promote or demote admins"""
    serializer_class = AdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    prermission_classes = (permissions.IsAdminUser,)

    def post(self, request, pk):
        admin = get_object_or_404(get_user_model(), pk=pk)
        admin.is_staff = not(admin.is_staff)
        admin.save()
        return Response(status=status.HTTP_200_OK)


class DeactiveAdmin(APIView):
    """The api view to active and deactivate admins"""
    serializer_class = AdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, pk):
        admin = get_object_or_404(get_user_model(), pk=pk)
        admin.is_active = not(admin.is_active)
        admin.save()
        return Response(status=status.HTTP_200_OK)
