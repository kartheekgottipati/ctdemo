"""Blockchain explorer """
import requests


def history(addr, offset):
    """Fetch hostory"""
    base_url = "https://blockchain.info"
    address_url = f"{base_url}/address/{addr}?format=json&offset={offset}"

    data = requests.get(address_url)
    return data.json()

