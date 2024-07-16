"""
Scan the chain for snapshot events on the Aave token
"""

api_url = 'http://127.0.0.1:8545'
start_block = 10926829
contract_address = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
outfile = "data/aave_token_events.csv"
#db_columns=["owner","oldValue","newValue"]
scanned_events = ["SnapshotDone"]

from tools.get_contract_events import getContractEvents
getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

#from get_contract_logs import getContractEvents

#target_events = ["SnapshotDone"]
#getContractEvents( contract_address, target_events, outfile, start_block, end_block=None )
