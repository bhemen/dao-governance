import requests
import pandas as pd

def get_comp_address_name(address):
    response = requests.get(f'https://api.compound.finance/api/v2/governance/accounts?addresses={address}')
    address_attributes = response.json()
    return address_attributes.get('accounts')[0].get('display_name')