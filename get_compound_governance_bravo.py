"""
Scan the chain for events from the Compound Governor Bravo contract
"""

api_url = 'http://127.0.0.1:8545'
start_block = 12006099 
contract_address = "0xc0Da02939E1441F497fd74F78cE7Decb17B66529"
outfile = "data/compound_governor_bravo.csv"
#db_columns=["id","proposer","targets","values","signatures","calldatas","startBlock","endBlock","description","voter","proposalId","support","votes","reason","eta","oldVotingDelay","newVotingDelay","oldVotingPeriod","newVotingPeriod","oldImplementation","newImplementation","oldProposalThreshold","newProposalThreshold","oldPendingAdmin","newPendingAdmin","oldAdmin","newAdmin"] #Note, the scraper is stupid, so these must match exactly the variable names in the smart contract
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["ProposalCreated","VoteCast","ProposalCanceled","ProposalQueued","ProposalExecuted","VotingDelaySet","VotingPeriodSet","NewImplementation","ProposalThresholdSet","NewPendingAdmin","NewAdmin"]

from tools.get_contract_events import getContractEvents

#getContractEvents(api_url,start_block,contract_address,outfile,db_columns,scanned_events)
getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

