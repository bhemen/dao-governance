"""
Scan the chain events from the UNI token
https://github.com/Uniswap/governance/blob/master/contracts/Uni.sol
"""

api_url = 'http://127.0.0.1:8545'
start_block = 10861674 
contract_address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
outfile = "data/uni_token_events_logs.csv"
#db_columns=["minter","newMinter","delegator","fromDelegate","toDelegate","delegate","previousBalance","newBalance","from","to","amount","owner","spender"]
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["MinterChanged","DelegateChanged","DelegateVotesChanged","Transfer","Approval"]

from tools.get_contract_events import getContractEvents
getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

#from get_contract_logs import getContractEvents

#target_events = []
#getContractEvents( contract_address, target_events, outfile, start_block, end_block=None )

