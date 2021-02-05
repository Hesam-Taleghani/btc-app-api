from rest_framework import serializers
from core.models import Country, POSCompany, PosModel, POS, VirtualService, MarketingGoal, \
     Costumer, Contract, ContractPOS, ContractService, PaperRoll, Payment, MIDRevenue
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
        read_only_fields = ['id', 'created_at', 'created_by']


class ServiceSerializer(serializers.ModelSerializer):
    """The virtual services serializer"""
    class Meta:
        model = VirtualService
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class GoalSerializer(serializers.ModelSerializer):
    """The Marketing goal serializer"""
    class Meta:
        model = MarketingGoal
        fields = ['id', 'trading_name', 'created_at', 'status', 'last_update', 'updated_at', 'business_field']
        read_only_fields = ['id', 'created_at', 'created_by', 'last_update', 'updated_at']


class GoalDetailSerializer(serializers.ModelSerializer):
    """The Serializer for goal's Details"""
    class Meta:
        model = MarketingGoal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class CostumerMiniSerializer(serializers.ModelSerializer):
    """The serializer for Costumer Suggestions"""
    class Meta:
        model = Costumer
        fields = ['id', 'legal_name', 'trading_name']
        read_only_fields = ['id']
    
class CostumerSerializer(serializers.ModelSerializer):
    """The serializer for managing Costumers"""
    class Meta:
        model = Costumer
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']


class ContractSerializer(serializers.ModelSerializer):
    """The Serializer for creating Contracts"""
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']


class ContractDetailSerializer(serializers.ModelSerializer):
    """The Serializer for managing Contracts and showin costumers"""
    costumer = CostumerSerializer(read_only=True)
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']


class ContractListSerializer(serializers.ModelSerializer):
    """The serializer for listing contracts"""
    legal_name = serializers.SerializerMethodField()
    trading_name = serializers.SerializerMethodField()
    business_type = serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = ['id', 'm_id', 'start_date', 'start_date', 'end_date', 'legal_name', 'trading_name', 'business_type']

    def get_legal_name(self, obj):
        return obj.costumer.legal_name

    def get_trading_name(self, obj):
        return obj.costumer.trading_name
    
    def get_business_type(self, obj):
        return obj.costumer.business_type
       


class ContractPosSerializer(serializers.ModelSerializer):
    """To Provide poses of a contract"""
    type = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    pos_model = serializers.SerializerMethodField()
    serial_number = serializers.SerializerMethodField()
    class Meta:
        model = ContractPOS
        fields = ['pos', 'id', 'price', 'hardware_cost', 'software_cost', 'type', 'company', 'pos_model', 'serial_number']
        read_only_fields = ['id']

    def get_type(self, obj):
        return obj.pos.type
    
    def get_company(self, obj):
        return str(obj.pos.model.company)

    def get_pos_model(self, obj):
        return str(obj.pos.model)
    
    def get_serial_number(self, obj):
        return str(obj.pos)

class ContractServiceSerializer(serializers.ModelSerializer):
    """To Provide services of a contract"""
    name = serializers.SerializerMethodField()
    class Meta:
        model = ContractService
        fields = ['service', 'id', 'price', 'cost', 'name']
        read_only_fields = ['id']

    def get_name(self, obj):
        return str(obj.service)


class CostumerPaperrollSerializer(serializers.ModelSerializer):
    """To Manage paper rolls of a costumer"""
    class Meta:
        model = PaperRoll
        fields = ['amount', 'cost', 'price', 'direct_debit_cost', 'ordered_date', 'id']
        read_only_fields = ['id']


class PaymentSerializer(serializers.ModelSerializer):
    """To manage Payments"""
    class Meta:
        model = Payment
        fields = ['id', 'date', 'direct_debit_cost']
        read_only_fields = ['id']


class MIDRevenueSerializer(serializers.ModelSerializer):
    """To manage mid revenues"""
    class Meta:
        model = MIDRevenue
        fields = ['id', 'income', 'profit', 'date']
        read_only_fields = ['id']
