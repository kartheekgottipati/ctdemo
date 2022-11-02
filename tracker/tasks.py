"""Celery tasks"""


from celery import shared_task
from tracker.coins.bitcoin import Bitcoin


@shared_task
def sync_transactions(address):
    """Fetch transactions"""
    btc = Bitcoin()
    btc.history(address)
    return True

