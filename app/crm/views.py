from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core import models
from crm import serializers

class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage Countries"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def filter_queryset(self, queryset):
        """To order the queryset in alphabet order of abreviations"""
        return self.queryset.order_by('abreviation')
    
    def perform_create(self, serializer):
        """To assign the admin to the country"""
        serializer.save(created_by=self.request.user)


class POSCompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage Companies"""
    serializer_class = (serializers.POSCompanySerializer)
    queryset = models.POSCompany.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """To assign the admin to the company"""
        serializer.save(created_by=self.request.user)
    
    def filter_queryset(self, queryset):
        """To order by name"""
        return self.queryset.order_by('name')