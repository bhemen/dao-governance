"""
Scan the chain for all events from the MKR chief
"""

api_url = 'http://127.0.0.1:8545'
start_block = 11327777 
contract_address = "0x0a3f6849f78076aefaDf113F5BED87720274dDC0"
outfile = "data/mkr_governance.csv"
db_columns=["slate","sig","guy","foo","bar","wad","fax","authority","owner"]
#MKR Glossary: https://docs.makerdao.com/other-documentation/system-glossary
scanned_events = ["Etch","LogSetAuthority","LogSetOwner","LogNote"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,db_columns,scanned_events)

