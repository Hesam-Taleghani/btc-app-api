from rest_framework import serializers
from core.models import Country, POSCompany, PosModel, POS, VirtualService, MarketingGoal
from django.core.exceptions import ValidationError


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
    model_count = serializers.SerializerMethodField()
    class Meta:
        model = POSCompany
        verbose_name_plural = 'Pos Companies'
        fields = ('id', 'name', 'serial_number_length', 'created_by', 'model_count')
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'model_count': {
                'read_only': True
            }
        }
    
    def get_model_count(self, instance):
        """To get the amount of models for a specific pos company"""
        return instance.pos_models.count()

    

class PosModelSerializer(serializers.ModelSerializer):
    """The POS model serializer"""
    class Meta:
        model = PosModel
        fields = ('id', 'name', 'hardware_cost', 'software_cost','price', 'created_by', 'company')
        extra_kwargs = {
            'id': {
                'read_only': True
            }, 
            'company': {
                'required': False
            }
        }


class PosSerializer(serializers.ModelSerializer):
    """The pos serializer"""
    class Meta:
        model = POS
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }, 
            'created_by': {
                'read_only': True
            }
        }


class ServiceSerializer(serializers.ModelSerializer):
    """The virtual services serializer"""
    class Meta:
        model = VirtualService
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }, 
            'created_by': {
                'read_only': True
            }
        }


class GoalSerializer(serializers.ModelSerializer):
    """The Marketing goal serializer"""
    class Meta:
        model = MarketingGoal
        fields = ['id', 'trading_name', 'created_at', 'status', 'last_update', 'updated_at', 'bussines_field']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }, 
            'created_by': {
                'read_only': True
            }, 
            'last_update': {
                'read_only': True
            }, 
            'updated_at': {
                'read_only': True
            }, 
        }


class GoalDetailSerializer(serializers.ModelSerializer):
    """The Serializer for goal's Details"""
    class Meta:
        model = MarketingGoal
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }, 
            'created_by': {
                'read_only': True
            }
        }
