from rest_framework import viewsets, mixins, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from core import models
from crm import serializers


class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """Base ViewSet To create, delete and list"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """To assign the admin to the Serializer"""
        serializer.save(created_by=self.request.user)

class CountryViewSet(BaseViewSet):
    """Manage Countries"""
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def filter_queryset(self, queryset):
        """To order the queryset in alphabet order of abreviations"""
        return self.queryset.order_by('abreviation')


class POSCompanyViewSet(BaseViewSet):
    """Manage Companies"""
    serializer_class = (serializers.POSCompanySerializer)
    queryset = models.POSCompany.objects.all()
    
    def filter_queryset(self, queryset):
        """To order by name"""
        return self.queryset.order_by('name')


class POSModelListView(generics.ListAPIView, mixins.DestroyModelMixin):
    """Manage pos models"""
    serializer_class = serializers.PosModelSerializer
    queryset = models.PosModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def filter_queryset(self, queryset):
        """To order by models"""
        return self.queryset.order_by('name')


class POSModelCreateView(generics.CreateAPIView):
    """Manage pos models"""
    serializer_class = serializers.PosModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        """To assign the admin and the company"""
        pk = self.kwargs.get('pk')
        company = get_object_or_404(models.POSCompany, pk=pk)
        serializer.save(created_by=self.request.user, company=company)


class PosModelCompanyList(generics.ListAPIView):
    """To retrieve models for a company"""
    serializer_class = serializers.PosModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """To return a filtered queryset"""
        pk = self.kwargs.get('pk')
        company = get_object_or_404(models.POSCompany, pk=pk)
        return models.PosModel.objects.filter(company=company)
    

class PosViewSet(BaseViewSet, mixins.UpdateModelMixin):
    """The view set to handle creating and listing poses"""
    queryset = models.POS.objects.all()
    serializer_class = serializers.PosSerializer

    def perform_create(self, serializer):
        """To assign the admin"""
        serial_number_length = serializer.validated_data['model'].company.serial_number_length
        if len(serializer.validated_data['serial_number']) != serial_number_length:
            raise ValidationError('Invalid Serial Number Length')
        else:
            serializer.save(created_by=self.request.user)

    def filter_queryset(self, queryset):
        """To order by serial number"""
        return self.queryset.order_by('serial_number')
    
    def partial_update(self, request, pk=None):
        """To check the serial number length for updating"""
        pos = get_object_or_404(models.POS, pk=pk)
        if len(request.data['serial_number']) != pos.model.company.serial_number_length:
            raise ValidationError('Invalid Serial Number Length')
        else:
            return super().partial_update(request, pk)


class ServiceViewSet(BaseViewSet, mixins.UpdateModelMixin):
    """The view set for virtual services"""
    queryset = models.VirtualService.objects.all()
    serializer_class = serializers.ServiceSerializer


class CountryIsUsed(APIView):
    """To check if the country is used"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """To return if the Country is used"""
        pk = kwargs.get('pk')
        country = get_object_or_404(models.Country, pk=pk)
        if (not(models.User.objects.filter(nationality=country).exists()) and 
           not(models.Costumer.objects.filter(country=country).exists()) and
           not(models.Costumer.objects.filter(director_nationality=country).exists()) and
           not(models.Costumer.objects.filter(partner_nationality=country).exists())):
            return Response(status=status.HTTP_200_OK, data={'used': False})
        else:
            return Response(status=status.HTTP_200_OK, data={'used': True})


class CompanyIsUsed(APIView):
    """To return if the poscompany is used"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """To return if the poscompany is used"""
        pk = kwargs.get('pk')
        company = get_object_or_404(models.POSCompany, pk=pk)
        if not(models.PosModel.objects.filter(company=company).exists()):
            return Response(status=status.HTTP_200_OK, data={'used': False})
        else:
            return Response(status=status.HTTP_200_OK, data={'used': True})


class PosModelIsUsed(APIView):
    """To return if the pos model is used"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """To return if the poscompany is used"""
        pk = kwargs.get('pk')
        model = get_object_or_404(models.PosModel, pk=pk)
        if not(models.POS.objects.filter(model=model).exists()):
            return Response(status=status.HTTP_200_OK, data={'used': False})
        else:
            return Response(status=status.HTTP_200_OK, data={'used': True})


class POSIsUsed(APIView):
    """To return if the pos is used"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """To return if the poscompany is used"""
        pk = kwargs.get('pk')
        pos = get_object_or_404(models.POS, pk=pk)
        if not(models.ContractPOS.objects.filter(pos=pos).exists()):
            return Response(status=status.HTTP_200_OK, data={'used': False})
        else:
            return Response(status=status.HTTP_200_OK, data={'used': True})


class ServiceIsUsed(APIView):
    """To return if the service is used"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """To return if the poscompany is used"""
        pk = kwargs.get('pk')
        service = get_object_or_404(models.VirtualService, pk=pk)
        if not(models.ContractService.objects.filter(service=service).exists()):
            return Response(status=status.HTTP_200_OK, data={'used': False})
        else:
            return Response(status=status.HTTP_200_OK, data={'used': True})


class ActivePos(APIView):
    """To handle activation of poses"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PosSerializer

    def post(self, request, pk):
        pos = get_object_or_404(models.POS, pk=pk)
        pos.is_active = not(pos.is_active)
        pos.save()
        return Response(status=status.HTTP_200_OK)


class GoalViewSet(viewsets.ModelViewSet):
    """To manage marketing goals"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GoalSerializer
    queryset = models.MarketingGoal.objects.all()

    def perform_create(self, serializer):
        """Create new Merketing Goal"""
        serializer.save(created_by=self.request.user, last_update=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate Serializer"""
        if self.action == "retrieve" or self.action == "update":
            return serializers.GoalDetailSerializer
        return self.serializer_class
    
    def perform_update(self, serializer):
        """To update the marketing goal"""
        serializer.save(last_update=self.request.user)


class CostumerListViewSet(generics.ListAPIView):
    """The viewset to handle the mini-list of Costumers"""
    serializer_class = serializers.CostumerMiniSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Costumer.objects.all()


class CostumerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """The viewset to handle creating and updating Costumers"""
    serializer_class = serializers.CostumerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Costumer.objects.all()

    def perform_create(self, serializer):
        """To assign the user"""
        serializer.save(created_by=self.request.user, last_updated_by=self.request.user)
    
    def perform_update(self, serializer):
        """To assign the user who has updated"""
        serializer.save(last_update_by=self.request.user)


class ContractViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """The viewset to handle creating and showing contracts"""
    serializer_class = serializers.ContractSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Contract.objects.all()

    def perform_create(self, serializer):
        """To assign the user"""
        serializer.save(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ContractListSerializer
        if self.action == 'retrieve':
            return serializers.ContractDetailSerializer
        return self.serializer_class


class ContractPosViewSet(generics.ListCreateAPIView):
    """To see and add poses of a contract"""
    serializer_class = serializers.ContractPosSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.ContractPOS.objects.all()

    def get_queryset(self):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        return models.ContractPOS.objects.filter(contract=contract)
    
    def perform_create(self, serializer):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        serializer.save(created_by=self.request.user, contract=contract)


class ContractServiceViewSet(generics.ListCreateAPIView):
    """To see and add virtual services of a contract"""
    serializer_class = serializers.ContractServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.ContractService.objects.all()

    def get_queryset(self):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        return models.ContractService.objects.filter(contract=contract)
    
    def perform_create(self, serializer):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        serializer.save(created_by=self.request.user, contract=contract)


class CostumerPaperRollViewSet(generics.ListCreateAPIView, generics.DestroyAPIView):
    """To list, create and delete PaperRolls of a costumer"""
    serializer_class = serializers.CostumerPaperrollSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.PaperRoll.objects.all()

    def get_queryset(self):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        costumer = contract.costumer
        return models.PaperRoll.objects.filter(costumer=costumer)
    
    def perform_create(self, serializer):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        costumer = contract.costumer
        serializer.save(created_by=self.request.user, costumer=costumer)


class PaymentViewSet(generics.ListCreateAPIView, generics.DestroyAPIView):
    """To see and add virtual services of a contract"""
    serializer_class = serializers.PaymentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Payment.objects.all()

    def get_queryset(self):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        return models.Payment.objects.filter(contract=contract)
    
    def perform_create(self, serializer):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        serializer.save(created_by=self.request.user, contract=contract)


class MIDViewSet(generics.ListCreateAPIView, generics.DestroyAPIView):
    """To see and add virtual services of a contract"""
    serializer_class = serializers.MIDRevenueSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Payment.objects.all()

    def get_queryset(self):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        return models.MIDRevenue.objects.filter(contract=contract)
    
    def perform_create(self, serializer):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(models.Contract, pk=contract_id)
        serializer.save(created_by=self.request.user, contract=contract)