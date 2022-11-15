from django.db import models
from django.conf import settings

# Create your models here.

class Address(models.Model):
    SYNC_CHOICES = [
        ("NEVER", "Never"),
        ("SCHEDULED", "Scheduled"),
        ("STARTED", "Started"),
        ("FAILED", "Failed"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=160)
    transaction_count = models.PositiveBigIntegerField(default=0)
    final_balance = models.PositiveBigIntegerField(default=0)
    last_successfull_sync = models.DateTimeField(null=True)
    sync_status = models.CharField(max_length=12, choices=SYNC_CHOICES, default="NEVER")

    def balance_in_btc(self):
        """Convert balance from SATS to BTC"""
        return self.final_balance * (10**-8)

    def __str__(self):
        return f"{self.address}"

    class Meta:
        unique_together = ('user', 'address')
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

class Transaction(models.Model):
    """Transaction model to keep track of transactions"""

    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    hash = models.CharField(max_length=255)
    inputs = models.JSONField(default=dict)
    out = models.JSONField(default=dict)
    fee = models.PositiveBigIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.hash}"

    class Meta:
        unique_together = ('address', 'hash')
