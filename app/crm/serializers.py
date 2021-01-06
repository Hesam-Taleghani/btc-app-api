from rest_framework import serializers
from core.models import Country, POSCompany


class CountrySerializer(serializers.ModelSerializer):
    """The Country serializer"""

    class Meta:
        model = Country
        verbose_name_plural = 'Countries'
        fields = ('id', 'name', 'code', 'abreviation', 'is_covered')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class POSCompanySerializer(serializers.ModelSerializer):
    """The pos company serializer"""

    class Meta:
        model = POSCompany
        verbose_name_plural = 'Pos Companies'
        fields = ('id', 'name', 'serial_number_length')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }