"""
Scan the chain for events from the Uniswap governor Alpha v2 contract
"""

api_url = 'http://127.0.0.1:8545'
start_block = 12543659 
contract_address = "0xC4e172459f1E7939D522503B81AFAaC1014CE6F6"
outfile = "data/uniswap_governor_alpha_v2.csv"
#db_columns=["id","proposer","targets","signatures","calldatas","startBlock","endBlock","description","voter","proposalId","support","votes","eta"] #Note, the scraper is stupid, so these must match exactly the variable names in the smart contract
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["ProposalCreated","VoteCast","ProposalCanceled","ProposalQueued","ProposalExecuted"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

