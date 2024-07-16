"""
Scan the chain for all events from a specific Curve Pool
"""

api_url = 'http://18.188.235.196:8545'
start_block = 10809473 #If you can find the block where the contract was deployed (e.g. using Etherscan) then we can safely start scraping events starting at this block height
contract_address = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
outfile = "data/curve_3pool.csv"
#db_columns=["buyer","sold_id","tokens_sold","bought_id","tokens_bought","provider","token_amounts","fees","invariant","token_supply","token_amount","coin_amount"] #Note, the scraper is stupid, so these must match exactly the variable names in the smart contract
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["TokenExchange","AddLiquidity","RemoveLiquidity","RemoveLiquidityOne","RemoveLiquidityImbalance"] 

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

