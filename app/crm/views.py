from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Country
from crm import serializers

class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Countries"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def filter_queryset(self,queryset):
        queryset = super(CountryViewSet, self).filter_queryset(queryset)
        return queryset.order_by('abreviation')