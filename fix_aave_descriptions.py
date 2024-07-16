import pandas as pd
import ast
from tqdm import tqdm
from analysis.ipfs_tools import bytesToIpfsHash, getFromIpfs
import json
import re

description_df = pd.read_csv( "data/aave_descriptions.csv")

bad_cids = ["QmPccptdeMjEAUbJLEXRw8s8dnWq6aVdigaqMUJGQJQBGV"]

def parseInvalidDescription(cid):
    d = str(getFromIpfs(cid))

    cols = ['basename', 'requires', 'discussions', 'updated', 'discussion', 'shortDescription', 'aip', 'title', 'preview', 'created', 'author', 'status', 'description']

    row = {}
    for c in cols:
        m = re.search( f"{c}:\s*(.+)", d )
        #m = re.search( f"title:\s*(\w+)", str(d))
        if m is not None:
            v = m[1].split("\\")[0]
            row[c] = v

    json_str = json.dumps(row).replace('"',"'")
    return json_str

print( description_df.dtypes )
description_df.loc[description_df.ipfsHash.isin(bad_cids),'description'] = description_df.loc[description_df.ipfsHash.isin(bad_cids),'ipfsHash'].apply(parseInvalidDescription)


#mask = (~description_df.ipfsHash.isna() & description_df.ipfsHash != "" )
#valid = description_df[mask]
#print( f"{valid.shape[0]} rows" )
#description_df.loc[mask,'description'] = valid['ipfsHash'].progress_apply(getFromIpfs)

#print( df.description.unique() )

description_df.to_csv( "data/aave_descriptions_fixed.csv", index=False )

#ipfshash = df.ipfsHash[~df.ipfsHash.isna()].iat[1] 

#print( ipfshash )

