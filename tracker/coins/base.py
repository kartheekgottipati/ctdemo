"""Explorers """
from datetime import datetime
from django.utils import timezone
from tracker.explorers import blockchain
from tracker.serializers import TransactionSerializer
from tracker.models import Address, Transaction


class BaseCoin:
    """Base coin"""

    coin_symbol = None
    display_name = None
    explorer = blockchain

    def process_txs(self, addr, txs):
        """Convert txs to be easy to store in db"""
        indexed_hashes = set(Transaction.objects.filter(address=addr).values_list('hash', flat=True))

        return [
            {
                "address": addr,
                "hash": tx["hash"],
                "fee": tx["fee"],
                "inputs": tx["inputs"],
                "out": tx["out"],
                "date": datetime.fromtimestamp(tx["time"]),
            }
            for tx in txs if tx['hash'] not in indexed_hashes
        ]

    def index_txs(self, txs):
        """Store in db"""
        serializer = TransactionSerializer(data=txs, many=True)
        if not serializer.is_valid():
            raise Exception("Serialization failed")

        serializer.save()

    def history(self, address):
        offset = 0

        try:
            address = Address.objects.get(address=address)
            address.sync_status = "STARTED"
            address.save()
        except Address.DoesNotExist as _:
            print(f"failed to sync the tranaction history for {address}")
            return False

        skip_balance_update = False
        while True:
            try:
                data = self.explorer.history(address, offset)
                if not skip_balance_update:
                    address.final_balance = data['final_balance']
                    address.transaction_count = data['n_tx']
                    address.save()

                txs = data["txs"]
                processed_txs = self.process_txs(address.pk, txs)
                self.index_txs(processed_txs)
                
                if len(txs) < 50:
                    break

                offset += 50
            except Exception as e:
                address.last_successfull_sync = timezone.now()
                address.sync_status = "FAILED"
                address.save()
                return False

        address.last_successfull_sync = timezone.now()
        address.sync_status = "COMPLETED"
        address.save()

