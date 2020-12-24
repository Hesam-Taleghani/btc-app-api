from rest_framework import serializers
from core.models import Country


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