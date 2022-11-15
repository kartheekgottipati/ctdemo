"""Tracker app views """
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from tracker.models import Address, Transaction
from tracker.tasks import sync_transactions
from tracker.coins.bitcoin import Bitcoin

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
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
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
        serializer = AddAddressSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            address = serializer.validated_data['address']
            try:
                btc = Bitcoin()
                basic_info = btc.fetch_basic_info(address)
            except Exception as e:
                return Response({"errors": e.message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(final_balance=basic_info["final_balance"], transaction_count=basic_info["transaction_count"])

            sync_transactions.delay(address)

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
        res = sync_transactions.delay(address_obj.address)
        return Response({"tast_id": res.task_id}, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ModelViewSet):
    """Transaction Model view set"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'address'
    filterset_fields = ['address__address']

    def list(self, request, *args, **kwargs):
        """List all addresses"""
        address = request.query_params.get('search')
        queryset = self.queryset.filter(address__user=request.user).filter(address__address=address)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
