"""Tracker app views """
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from tracker.models import Address, Transaction
from tracker.tasks import sync_transactions

from tracker.serializers import (
    AddressSerializer,
    AddAddressSerializer,
    TransactionSerializer,
)

# Create your views here.


class AddressViewSet(viewsets.ViewSet):
    """Address Model view set"""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "address"

    def list(self, request):
        """List all addresses"""
        queryset = self.queryset
        addresses = queryset.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Add new address"""
        serializer = AddAddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            sync_transactions.delay(serializer.data["address"])

            address = serializer.data["address"]
            address_obj = self.queryset.get(address=address)
            address_obj.sync_status = "SCHEDULED"
            address_obj.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, address=None):
        """Retrieve a single address"""
        queryset = Address.objects.all()
        address = get_object_or_404(queryset, address=address)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def update(self, request, address):  # pylint: disable=W0613
        """Update an address information"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, address):  # pylint: disable=W0613
        """Partially update an address information"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, address):
        """Delete the address provided"""
        try:
            instance = Address.objects.get(address=address)
            instance.delete()
        except self.queryset.model.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def sync_transactions(self, request, address=None):
        address_obj = get_object_or_404(self.queryset, address=address)
        if address_obj.sync_status == "SCHEDULED":
            return Response({"msg": "sync already scheduled"}, status=status.HTTP_200_OK)

        res = sync_transactions.delay(address)
        return Response({"tast_id": res.task_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def reset_sync_status(self, request, address=None):
        address_obj = get_object_or_404(self.queryset, address=address)
        address_obj.sync_status == "COMPLETED"
        address_obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class TransactionViewSet(viewsets.ModelViewSet):
    """Transaction Model view set"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'address'

class IndexView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request):
        queryset = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
