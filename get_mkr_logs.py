from web3 import Web3
import progressbar
import pandas as pd
from utils import get_cached_abi
from get_contract_logs import getContractEvents

mkr_chief = "0x0a3f6849f78076aefaDf113F5BED87720274dDC0"
deploy_block = 11327777 
outfile = "data/mkr_chief_logs.csv"
target_events = 'all'

getContractEvents( mkr_chief, target_events, outfile, deploy_block,end_block=None )


