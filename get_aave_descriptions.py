import pandas as pd
import ast
from tqdm import tqdm
from analysis.ipfs_tools import bytesToIpfsHash, getFromIpfs
import json

####
#Convert stringified bytes to ipfs Hash
###

filename = "data/aave_governance_v2.csv"
df = pd.read_csv(filename,dtype={'ipfsHash':str})
df['ipfsHash'].replace(to_replace='',value=None,inplace=True)
df['ipfsHash'].fillna(value='',inplace=True)

#df['ipfsHash'] = df['ipfsHash'].apply( ast.literal_eval )

#print( ast.literal_eval(df.ipfsHash[75] ) )
print( df.ipfsHash[75] )

bytesToIpfsHash(df.ipfsHash[75])

#print( df.ipfsHash.unique() )

df['ipfsHash'] = df['ipfsHash'].apply( bytesToIpfsHash )

df.to_csv(filename,index=False)

print( df.ipfsHash.unique() )

###
#Fetch data from ipfs
###

tqdm.pandas()

description_df = pd.DataFrame( {'ipfsHash': df.ipfsHash} )
description_df.dropna(inplace=True) #Most rows don't have an ipfsHash
description_df = description_df[description_df.ipfsHash != ""]

description_df['description'] = description_df.ipfsHash.progress_apply(getFromIpfs)


#mask = (~description_df.ipfsHash.isna() & description_df.ipfsHash != "" )
#valid = description_df[mask]
#print( f"{valid.shape[0]} rows" )
#description_df.loc[mask,'description'] = valid['ipfsHash'].progress_apply(getFromIpfs)

#print( df.description.unique() )

description_df.to_csv( "data/aave_descriptions.csv", index=False )

#ipfshash = df.ipfsHash[~df.ipfsHash.isna()].iat[1] 

#print( ipfshash )

