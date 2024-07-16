"""
Scan the chain for events from the Uniswap Governor Bravo Contract
"""

api_url = 'http://127.0.0.1:8545'
start_block = 13059157 
contract_address = "0x408ED6354d4973f66138C91495F2f2FCbd8724C3"
outfile = "data/uniswap_governor_bravo.csv"
#db_columns=["id","proposer","targets","values","signatures","calldatas","startBlock","endBlock","description","voter","proposalId","support","votes","reason","eta","oldVotingDelay","newVotingDelay","oldVotingPeriod","newVotingPeriod","oldImplementation","newImplementation","oldProposalThreshold","newProposalThreshold","oldPendingAdmin","newPendingAdmin","oldAdmin","newAdmin"] #Note, the scraper is stupid, so these must match exactly the variable names in the smart contract
#abi = get_cached_abi(contract_address)
#contract = web3.eth.contract(abi=abi)
#scanned_events = [contract.events.TokenExchange,contract.events.AddLiquidity,contract.events.RemoveLiquidity,contract.events.RemoveLiquidityOne,contract.events.RemoveLiquidityImbalance] 
scanned_events = ["ProposalCreated","VoteCast","ProposalCanceled","ProposalQueued","ProposalExecuted","VotingDelaySet","VotingPeriodSet","NewImplementation","ProposalThresholdSet","NewPendingAdmin","NewAdmin"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

