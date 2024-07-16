"""
Convert events from Lido and Aave into the same format used by Compound
Note that since Uniswap copied Compound's governance contracts, Uniswap data is already in the same format as Compound

Required by data_viz.ipynb
"""

import pandas as pd
import numpy as np
import os
from ipfs_tools import bytesToIpfsHash

#In Compound / Uniswap, when a Proposal is created it's given an 'id'
#When a vote is cast on Proposal, the vote has a 'proposalId'
#So 'id's are set on proposal creations, but not votes

def convert_lido(lido_governance):
    df = pd.read_csv(lido_governance)
    df = df.rename(columns={'supports': 'support','stake': 'votes', 'metadata': 'description','voteId':'proposalId'})
    df['id'] = np.where(df['event_name'] != 'CastVote', df['proposalId'], np.nan)
    df['event_name'] = df['event_name'].replace('CastVote', 'VoteCast')
    # # df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)

    return df

def convert_aave(aave_governance):
    df = pd.read_csv(aave_governance)
    df = df.rename(columns={'votingPower': 'votes','ipfsHash': 'ipfsHashBytes'})
    df['proposalId'] = df['id']
    df['event_name'] = df['event_name'].replace('VoteEmitted', 'VoteCast')
    # df['timestamp'] = df['timestamp'].apply(datetime.fromtimestamp)
    
    df['ipfsHash'] = df['ipfsHashBytes'].apply( bytesToIpfsHash )
    if os.path.isfile( "../data/aave_descriptions_parsed.csv" ):
        description_df = pd.read_csv( "../data/aave_descriptions_parsed.csv" )
        df = df.merge( description_df, how='left', on='ipfsHash' )
    return df

def parse_event_csv(csv_name):
    if 'lido' in csv_name:
        df = convert_lido(csv_name)
    elif 'aave' in csv_name:
        df = convert_aave(csv_name)
    else:
        df = pd.read_csv(csv_name, 
                usecols = ['event_name','block_number','timestamp','votes','voter','proposalId','id','support','description' ],
                dtype={'event_name': str, 'block_number': int, 'timestamp': str, 'id': float, 'voter': str, 'votes': float, 'proposalId': float,'support':float } )

    df['votes'] = df['votes'].astype(float) / 1e18

    if 'id' in df.columns:
        df['proposalId'] = np.where(df['proposalId'].isnull(), df['id'], df['proposalId'] )
    
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S')
        df['days_from_start'] = (df['timestamp'] - df['timestamp'][0]).dt.days
        
    # duplicate proposal ids in Uniswap
    if 'uniswap_governor_alphav2' in csv_name:
        df['proposalId'] = df['proposalId'] + 4
        df['id'] = df['id'] + 4
    
    
    #df['description'] = df.groupby(['proposalId'],sort=False)['description'].apply( lambda x: x.ffill().bfill() )
    return df
