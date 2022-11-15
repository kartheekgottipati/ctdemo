from django.contrib import admin
from tracker.models import Address, Transaction
# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
