import requests, json
import pandas as pd
import numpy as np
import time

def get_compound_name(address,wait_time=60,retry=0):
    compound_names = "../data/compound_names.csv"
    max_retries = 3
    try:
        comp_df = pd.read_csv(compound_names)
    except Exception as e:
        comp_df = pd.DataFrame(columns=['address','name','timestamp'])
    
    names = comp_df[comp_df.address==address].sort_values(by='timestamp',ascending=False)
    
    if names.shape[0] >= 1:
        return names.name.iat[-1]
    
    try:
        response = requests.get(f'https://api.compound.finance/api/v2/governance/accounts?addresses={address}')
    except Exception as e:
        print( f"Error connecting to Compound API (address = {address})" )
        print( e )
        return np.nan
    try:
        address_attributes = response.json()
    except Exception as e:
        if response.status_code == 429:
            print( f"Too many queries to the Compound API: retrying in {wait_time}s" )
            if retry > max_retries:
                return np.nan
            time.sleep(wait_time)
            return get_compound_name(address,wait_time=wait_time*2,retry=retry+1)
        print( "get_compound_names: Error jsonifying" )
        return np.nan
    if address_attributes.get('accounts'):
        name = address_attributes.get('accounts')[0].get('display_name')
        comp_df = pd.concat( [comp_df, pd.DataFrame( [{'address':address,'name':name,'timestamp': time.time()}] )] )
        comp_df.to_csv(compound_names,index=False)
    else:
        return np.nan

def make_compound_names_df():
    compound_names = pd.read_csv("../data/compound_names.csv")
    compound_names = compound_names.groupby('address').last().reset_index()
    compound_names = compound_names[['address','name']]
    compound_names.rename( columns={'address': 'voter', 'name':'compound_name'},inplace=True)

    return compound_names
    

def make_ens_names_df():
    ens_names_etherscan = pd.read_csv("../data/ens_names_etherscan.csv")
    ens_names_ns = pd.read_csv("../data/ens_names_ns.csv")

    ens_names = pd.concat([ens_names_etherscan, ens_names_ns], ignore_index=True)
    ens_names.rename(columns={'address': 'voter', 'name': 'ens_name'}, inplace=True)

    return ens_names

def make_sybil_names_df():
    url = "https://raw.githubusercontent.com/Uniswap/sybil-list/master/verified.json"
    r = requests.get(url)
    sybil_dict = json.loads(r.text)
    sybil = pd.DataFrame.from_dict(sybil_dict, orient='index')

    sybil_twitter = sybil['twitter'].apply(pd.Series)
    sybil_other = sybil['other'].apply(pd.Series)

    sybil = sybil.merge(sybil_twitter, left_index=True, right_index=True)
    sybil = sybil.merge(sybil_other, left_index=True, right_index=True)
    sybil.drop(columns=['twitter', 'other', '0_x', 'timestamp', 'tweetID', '0_y', 'contentURL'], inplace=True)
    sybil = sybil.reset_index(level=0)
    sybil['handle'].fillna(sybil['name'], inplace=True)
    sybil.drop(columns=['name'], inplace=True)
    sybil.columns = ['voter', 'sybil_name']

    return sybil
