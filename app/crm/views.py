from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Country
from crm import serializers

class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage Countries"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def filter_queryset(self,queryset):
        """To order the queryset in alphabet order of abreviations"""
        return self.queryset.order_by('abreviation')
    
    def perform_create(self, serializer):
        """To assign the admin to the country"""
        serializer.save(created_by=self.request.user)
