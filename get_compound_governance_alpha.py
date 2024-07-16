"""
Scan the chain for events from the Compound Governor Alpha contract
https://github.com/compound-finance/compound-protocol/blob/master/contracts/Governance/GovernorAlpha.sol
"""

api_url = 'http://127.0.0.1:8545'
start_block = 9601459 
contract_address = "0xc0dA01a04C3f3E0be433606045bB7017A7323E38"
outfile = "data/compound_governor_alpha.csv"
#db_columns=["id","proposer","targets","signatures","calldatas","startBlock","endBlock","description","voter","proposalId","support","votes","eta"] #Note, the scraper is stupid, so these must match exactly the variable names in the smart contract
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["ProposalCreated","VoteCast","ProposalCanceled","ProposalQueued","ProposalExecuted"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

