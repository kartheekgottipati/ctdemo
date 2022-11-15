"""Celery tasks"""

from celery import shared_task, states
from celery.utils.log import get_task_logger
from tracker.coins.bitcoin import Bitcoin
from tracker.models import Address, Transaction

logger = get_task_logger(__name__)

@shared_task(bind=True)
def sync_transactions(self, address):
    """Fetch transactions"""
    btc = Bitcoin()
    try:
        btc.fetch_all_transactions(wallet_address=address)
    except Exception as ex:
        self.update_state(state=states.FAILURE)
        logger.error(ex)
        raise
    return True


@shared_task(bind=True)
def sync_transactions_after_most_recent_tx_date(self, address):
    """Fetch transactions after the most recent tx date in database"""
    try:
        address_obj = Address.objects.get(address=address)
        recent_tx = Transaction.objects.filter(
            address=address_obj).order_by('-date').first()
        date_since = recent_tx.date

        btc = Bitcoin()
        btc.fetch_transactions_after_a_recent_tx_date(
            wallet_address=address, date_since=date_since)
    except Exception as ex:
        self.update_state(state=states.FAILURE)
        logger.error(ex)
        raise
    return True


@shared_task(bind=True)
def schedule_sync_for_all_addresses(self):
    """Fetch all the addresses from the database and add the
    sync_transaction task to queue"""
    
    addresses = Address.objects.all()
    
    print(f"posting {len(addresses)} addresses")

    for address_obj in addresses:
        sync_transactions.delay(address_obj.address)

    return True
