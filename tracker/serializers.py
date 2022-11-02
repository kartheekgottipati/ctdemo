"""Tracker model serializers """
from django.db import IntegrityError
from rest_framework import serializers, status

from tracker.models import Address, Transaction


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    class Meta:
        """Address Serializer meta class"""

        model = Address
        fields = "__all__"


class AddAddressSerializer(serializers.ModelSerializer):
    """Serializer for Adding new address to model"""

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        """Add address serializer meta class"""

        model = Address
        fields = ["address", "user", 'transaction_count', 'final_balance', 'last_successfull_sync', 'sync_status']
        read_only_fields = ['transaction_count', 'final_balance', 'last_successfull_sync', 'sync_status']
    
    def validate(self, attrs):
        address = attrs.get('address')
        user = self.context.get('request').user
        try:
            Address.objects.get(address=address, user=user)
            raise serializers.ValidationError({"msg": "this address already exist"}, code=status.HTTP_400_BAD_REQUEST)

        except Address.DoesNotExist as e:
            pass

        attrs["user"] = user
        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""

    class Meta:
        """Transaction serializer meta class"""

        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        created_ids = []
        for tx in validated_data:
            try:
                created = super().create(tx)
                created_ids.append(created.pk)
            except IntegrityError:
                pass
        return super().create(validated_data)
