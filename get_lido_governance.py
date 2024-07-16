"""
Scan the chain for events from the Lido Governance Contract
"""

api_url = 'http://127.0.0.1:8545'
start_block = 11473216 
contract_address = "0x2e59A20f205bB85a89C53f1936454680651E618e" #Note this is a proxy, but utils.py can still find its abi on Etherscan
outfile = "data/lido_governance.csv"

from tools.get_contract_events import getContractEvents
scanned_events = "all"

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

#from get_contract_logs import getContractEvents

#target_events = []
#getContractEvents( contract_address, target_events, outfile, start_block, end_block=None )

