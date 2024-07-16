"""
Scan the chain for events from the Aave Governance V2 Contract
The contract interface can be found https://github.com/aave/governance-v2/blob/master/contracts/interfaces/IAaveGovernanceV2.sol
"""

api_url = 'http://127.0.0.1:8545'
start_block = 11427398 
contract_address = "0xEC568fffba86c094cf06b22134B23074DFE2252c"
outfile = "data/aave_governance_v2.csv"
#db_columns=["id","creator","executor","targets","values","signatures","calldatas","withDelegateCalls","startBlock","endBlock","strategy","ipfsHash","executionTime","initiatorQueuing","initiatorExecution","voter","support","votingPower","newStrategy","initiatorChange","newVotingDelay"]
#scanned_events = ["ProposalCreated","ProposalCanceled","ProposalQueued","ProposalExecuted","VoteEmitted","GovernanceStrategyChanged","VotingDelayChanged","ExecutorAuthorized","ExecutorUnauthorized"]

#from tools.get_contract_events import getContractEvents

#getContractEvents(api_url,start_block,contract_address,outfile,db_columns,scanned_events)

#from get_contract_logs import getContractEvents

#target_events = []
#getContractEvents( contract_address, target_events, outfile, start_block, end_block=None )


scanned_events = 'all'
from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)
