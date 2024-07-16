"""
Scan the chain for events from the COMP token contract
"""

api_url = 'http://127.0.0.1:8545'
start_block = 9601359
contract_address = "0xc00e94Cb662C3520282E6f5717214004A7f26888"
outfile = "data/comp_token_events.csv"
#db_columns=["delegate","delegator","fromDelegate","toDelegate","previousBalance","newBalance","from","to","amount","owner","spender"]
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["DelegateChanged","DelegateVotesChanged","Transfer","Approval"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

