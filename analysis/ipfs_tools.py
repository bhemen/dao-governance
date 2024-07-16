"""
Required by convert_to_compound.py
"""

import pandas as pd
import base58
import ast
import time
import requests
import random

def bytesToIpfsHash(x):
    if x is None or x == "nan" or pd.isna(x):
        return None
   
    if type(x) == str:
        if len(x) > 2:
            if x[0:2] == "b'" or x[0:2] == 'b"':
                try:
                    y = ast.literal_eval(x)
                except Exception as e:
                    print( e )
                    return None
            else:
                return x
        else:
            return x
    
    if type(x) == bytes:
        y = x
            
    try:
        CID = base58.b58encode( bytes.fromhex( "1220" + y.hex() ) )
    except Exception as e:
        print( e )
        return None
    return CID.decode('utf-8')

def getFromIpfs(cid,content_type="json"):

    if cid is None or cid == "":
        return None

    #https://luke.lol/ipfs.php
    gateways = ['https://ipfs.io/ipfs/','https://cloudflare-ipfs.com/ipfs/','https://gateway.ipfs.io/ipfs/','https://gateway.pinata.cloud/ipfs/','https://hardbin.com/ipfs/']
    #gateways = ['https://ipfs.io/ipfs/','https://cf-ipfs.com/ipfs/','https://cloudflare-ipfs.com/ipfs/','https://gateway.ipfs.io/ipfs/','https://gateway.pinata.cloud/ipfs/','https://hardbin.com/ipfs/']

    i = random.randint( 0, len(gateways)-1 ) 
    date = None
    for j in range(len(gateways)):
        gateway_url = gateways[(i+j)%len(gateways)]
        try:
            data = getFromGateway(cid,gateway_url,content_type)
        except Exception as e:
            print( f"Error in getFromIpfs ({gateway_url})" )
            print( e )
            continue
       
        if data is not None:
            print( f"Success on {gateway_url}" )
            return data
      
    print( f"Failed to get data for {cid}" )
    return None

def getFromGateway(cid,gateway_url,content_type="json",retries=0,sleep_time=5):
    start = time.time()
    response = requests.get(gateway_url + cid )
    end = time.time()

    if response.status_code == 429:
        print( f"{gateway_url} Rate limit" )
        if retries < 5:
            print( f"Waiting {sleep_time}s" )
            time.sleep(sleep_time)
            return getFromGateway(cid,gateway_url,content_type,retries=retries+1,sleep_time=sleep_time*2)
        else:
            return None

    if response.status_code != 200:
        print( f"Error Reading from {gateway_url}" )
        print( f"Status Code = {response.status_code}" )
        return None

    if content_type == "json":
        try:
            content = response.json()
        except Exception as e:
            print( f"IPFS did not return valid json" )
            print( response.text )
    if content_type == "bytes":
        #content = response.raw.read()
        content = response.content

    #print( f"Getting with Gateway took {end-start}s" )
    return response.content


